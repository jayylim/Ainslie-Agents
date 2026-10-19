"""
Interactive mini web app for the "Max SS resisted vs stickiness" graph.

Same model as visual_demos/sticky_graph.py: one curve per LL delay, overlaid.
Sliders let you change:

    - LL delay max / step   (which delays to plot; same idea as ll_delays)
    - LL magnitude          (shared reward value for every curve)

Move any slider and the family of curves redraws live. Maths is computed in
Python (agents/hyperbolic.py + sticky_decisions.stick_p_t) so results match
the static script; the browser draws the returned points with Plotly.

Run from the package root:

    python -m visual_demos.sticky_web_app

then open the printed URL (default http://127.0.0.1:5000).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from flask import Flask, jsonify, render_template_string, request

from agents.hyperbolic import HypAgent
from environments.timeline import TimelineEnvironment
from main import agent_params, env_params
from sticky_decisions import stick_p_t

# === Stickiness sweep (x-axis) ===
STICKINESS_MIN, STICKINESS_MAX, N_STICKINESS_POINTS = 0.0, 1.0, 100

# Defaults match sticky_graph.py: ll_delays = list(range(0, 25, 4))
DEFAULT_DELAY_MAX = 24
DEFAULT_DELAY_STEP = 4
DEFAULT_MAGNITUDE_LL = env_params["rewards"]["LL"]["value"]

# Build the agent/environment once; the sliders only change numbers fed into
# the value function, so there is no need to rebuild anything per request.
environment = TimelineEnvironment(**env_params)
agent = HypAgent(**agent_params)
state = environment.reset()

HORIZON = agent.get_horizon(state, environment)
DECISION_INTERVAL = environment.decision_interval
DISCOUNT_FACTOR = agent.discount_factor
DELAY_SS = environment.rewards["SS"]["delay"]


def max_ss_resisted(s, delay_LL, reward_LL):
    """
    Maximum SS such that V(resist) >= V(snack) under stickiness s (LL fixed).

    Identical derivation to visual_demos/sticky_graph.max_ss_resisted:
        x = reward_LL * (V_resist_LL - V_snack_LL) / (V_snack_SS - V_resist_SS)
    """
    V_resist_LL = 0.0
    V_resist_SS = 0.0
    V_snack_LL = 0.0
    V_snack_SS = 0.0

    for t in range(HORIZON):
        sticking = stick_p_t(s, t)

        v_SS = agent.value_function(1.0, DELAY_SS + t * DECISION_INTERVAL)
        v_LL = agent.value_function(1.0, delay_LL + t * DECISION_INTERVAL)

        # resist today: same = LL, other = SS
        V_resist_LL += sticking * v_LL
        V_resist_SS += (1.0 - sticking) * v_SS

        # snack today: same = SS, other = LL
        V_snack_SS += sticking * v_SS
        V_snack_LL += (1.0 - sticking) * v_LL

    denom = V_snack_SS - V_resist_SS
    if denom == 0:
        return None  # JSON-safe; Plotly skips null points
    return reward_LL * (V_resist_LL - V_snack_LL) / denom


def stickiness_axis():
    step = (STICKINESS_MAX - STICKINESS_MIN) / (N_STICKINESS_POINTS - 1)
    return [STICKINESS_MIN + i * step for i in range(N_STICKINESS_POINTS)]


def delay_list(delay_max, delay_step):
    """Same spirit as sticky_graph: list(range(0, delay_max + 1, delay_step))."""
    delay_max = max(0, int(delay_max))
    delay_step = max(1, int(delay_step))
    return list(range(0, delay_max + 1, delay_step))


app = Flask(__name__)


@app.route("/api/curves")
def api_curves():
    delay_max = request.args.get("delay_max", DEFAULT_DELAY_MAX, type=float)
    delay_step = request.args.get("delay_step", DEFAULT_DELAY_STEP, type=float)
    reward_LL = request.args.get("magnitude", DEFAULT_MAGNITUDE_LL, type=float)

    delays = delay_list(delay_max, delay_step)
    xs = stickiness_axis()
    curves = [
        {
            "delay_LL": d,
            "max_ss": [max_ss_resisted(s, d, reward_LL) for s in xs],
        }
        for d in delays
    ]

    return jsonify(
        {
            "stickiness": xs,
            "curves": curves,
            "delays": delays,
            "reward_LL": reward_LL,
            "horizon": HORIZON,
            "discount_factor": DISCOUNT_FACTOR,
        }
    )


PAGE = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Max SS resisted — interactive</title>
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
<style>
  :root { --fg:#1b2430; --muted:#5a6b7b; --accent:#2a6df4; --bg:#f5f7fb; }
  * { box-sizing: border-box; }
  body {
    margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: var(--fg); background: var(--bg);
  }
  .wrap { max-width: 980px; margin: 0 auto; padding: 24px 20px 48px; }
  h1 { font-size: 20px; margin: 0 0 4px; }
  .sub { color: var(--muted); font-size: 13px; margin: 0 0 20px; }
  .controls {
    display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px;
    background: #fff; border: 1px solid #e3e8ef; border-radius: 12px;
    padding: 18px 20px; margin-bottom: 18px;
  }
  @media (max-width: 780px) { .controls { grid-template-columns: 1fr; } }
  .ctrl label { display: flex; justify-content: space-between; align-items: baseline;
    font-size: 13px; font-weight: 600; margin-bottom: 8px; }
  .ctrl label .val { color: var(--accent); font-variant-numeric: tabular-nums; }
  input[type=range] { width: 100%; accent-color: var(--accent); }
  .range-row { display: flex; justify-content: space-between; color: var(--muted);
    font-size: 11px; margin-top: 4px; }
  #chart { background:#fff; border:1px solid #e3e8ef; border-radius:12px; padding:8px; }
  .meta { color: var(--muted); font-size: 12px; margin-top: 10px; }
</style>
</head>
<body>
<div class="wrap">
  <h1>Max SS resisted vs stickiness</h1>
  <p class="sub">One curve per LL delay (like <code>sticky_graph.py</code>).
     Change delay range / step or LL magnitude and the overlay updates.</p>

  <div class="controls">
    <div class="ctrl">
      <label for="delayMax">LL delay max (hours) <span class="val" id="delayMaxVal"></span></label>
      <input type="range" id="delayMax" min="0" max="48" step="1" />
      <div class="range-row"><span>0</span><span>48</span></div>
    </div>
    <div class="ctrl">
      <label for="delayStep">LL delay step (hours) <span class="val" id="delayStepVal"></span></label>
      <input type="range" id="delayStep" min="1" max="12" step="1" />
      <div class="range-row"><span>1</span><span>12</span></div>
    </div>
    <div class="ctrl">
      <label for="mag">LL magnitude (reward) <span class="val" id="magVal"></span></label>
      <input type="range" id="mag" min="1" max="40" step="0.5" />
      <div class="range-row"><span>1</span><span>40</span></div>
    </div>
  </div>

  <div id="chart"></div>
  <p class="meta" id="meta"></p>
</div>

<script>
const DEFAULT_DELAY_MAX = {{ default_delay_max }};
const DEFAULT_DELAY_STEP = {{ default_delay_step }};
const DEFAULT_MAG = {{ default_mag }};

const delayMaxEl = document.getElementById("delayMax");
const delayStepEl = document.getElementById("delayStep");
const magEl = document.getElementById("mag");
const delayMaxValEl = document.getElementById("delayMaxVal");
const delayStepValEl = document.getElementById("delayStepVal");
const magValEl = document.getElementById("magVal");
const metaEl = document.getElementById("meta");

delayMaxEl.value = DEFAULT_DELAY_MAX;
delayStepEl.value = DEFAULT_DELAY_STEP;
magEl.value = DEFAULT_MAG;

let plotted = false;

function syncLabels() {
  delayMaxValEl.textContent = delayMaxEl.value + "h";
  delayStepValEl.textContent = delayStepEl.value + "h";
  magValEl.textContent = magEl.value;
}

function yMaxFrom(data) {
  let m = 0;
  for (const c of data.curves) {
    for (const v of c.max_ss) {
      if (Number.isFinite(v) && v > m) m = v;
    }
  }
  // Room above the curves, at least as tall as the old fixed [0, 8] view.
  return Math.max(8, Math.ceil(m * 1.15));
}

function draw(data) {
  if (typeof Plotly === "undefined") {
    metaEl.textContent = "Plotly failed to load (CDN blocked?). Refresh or check network.";
    return;
  }
  const ymax = yMaxFrom(data);
  const traces = data.curves.map((c) => ({
    x: data.stickiness,
    y: c.max_ss,
    mode: "lines",
    line: { width: 2.5 },
    name: `LL delay = ${c.delay_LL}h`,
  }));
  // uirevision changes with the sliders so a prior zoom does not hide curves
  // after a parameter change. Same params => zoom/pan is kept while exploring.
  const uirevision =
    `${delayMaxEl.value}|${delayStepEl.value}|${magEl.value}|${ymax}`;
  const layout = {
    margin: { l: 60, r: 20, t: 40, b: 80 },
    xaxis: { title: "Stickiness s", range: [0, 1], autorange: false, zeroline: false },
    yaxis: { title: "Max SS resisted", range: [0, ymax], autorange: false,
             gridcolor: "#eef1f6" },
    uirevision: uirevision,
    dragmode: "zoom",
    height: 520,
    showlegend: true,
    legend: { orientation: "h", y: -0.22 },
    font: { family: "-apple-system, Segoe UI, Roboto, sans-serif", size: 12 },
  };
  // Box-zoom / pan / reset via toolbar. No scroll-zoom (easy to trap a bad view).
  const opts = {
    responsive: true,
    displayModeBar: true,
    displaylogo: false,
    scrollZoom: false,
    modeBarButtonsToRemove: ["lasso2d", "select2d"],
  };
  if (!plotted) {
    Plotly.newPlot("chart", traces, layout, opts);
    plotted = true;
  } else {
    Plotly.react("chart", traces, layout, opts);
  }
  metaEl.textContent =
    `delays = [${data.delays.join(", ")}]h · LL magnitude = ${data.reward_LL} · ` +
    `horizon = ${data.horizon} · discount_factor = ${data.discount_factor} · ` +
    `drag to zoom · double-click or home icon to reset`;
}

let timer = null;
async function update() {
  syncLabels();
  const url =
    `/api/curves?delay_max=${delayMaxEl.value}` +
    `&delay_step=${delayStepEl.value}` +
    `&magnitude=${magEl.value}`;
  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error("HTTP " + res.status);
    draw(await res.json());
  } catch (err) {
    metaEl.textContent = "Failed to load curves: " + err +
      " — is the Flask server still running on http://127.0.0.1:5000 ?";
  }
}

function schedule() {
  syncLabels();
  clearTimeout(timer);
  timer = setTimeout(update, 40);
}

delayMaxEl.addEventListener("input", schedule);
delayStepEl.addEventListener("input", schedule);
magEl.addEventListener("input", schedule);
update();
</script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(
        PAGE,
        default_delay_max=DEFAULT_DELAY_MAX,
        default_delay_step=DEFAULT_DELAY_STEP,
        default_mag=DEFAULT_MAGNITUDE_LL,
    )


if __name__ == "__main__":
    import webbrowser

    url = "http://127.0.0.1:5000"
    print(f"Serving interactive sticky graph at {url}")
    print("Open that URL in Chrome/Safari (not only the Cursor preview).")
    try:
        webbrowser.open(url)
    except Exception:
        pass
    # use_reloader=False avoids a second process fighting the debugger for port 5000
    app.run(debug=False, host="127.0.0.1", port=5000, use_reloader=False)
