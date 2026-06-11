const data = window.REPORT_DATA;

const state = {
  domain: "all",
  tier: "all",
  provider: "all",
  selectedModel: null,
  query: "",
};

const fmtPct = (value) => `${value.toFixed(1)}%`;
const byId = (id) => document.getElementById(id);
const escapeHtml = (value) => String(value)
  .replaceAll("&", "&amp;")
  .replaceAll("<", "&lt;")
  .replaceAll(">", "&gt;")
  .replaceAll('"', "&quot;");

/* ---- scroll-in animation: numbers tick up, bars grow, heat cells fade in.
   Each container animates once, on first reveal; filter re-renders after that
   paint final values directly. Reduced-motion users get instant finals. ---- */

const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const revealedSections = new Set();
const easeOutCubic = (t) => 1 - Math.pow(1 - t, 3);

function animateCount(el) {
  const target = parseFloat(el.dataset.count);
  const decimals = parseInt(el.dataset.decimals || "0", 10);
  const suffix = el.dataset.suffix || "";
  const done = () => { el.textContent = target.toFixed(decimals) + suffix; };
  if (reduceMotion) { done(); return; }
  const dur = 700;
  const start = performance.now();
  const tick = (now) => {
    const t = Math.min((now - start) / dur, 1);
    el.textContent = (target * easeOutCubic(t)).toFixed(decimals) + suffix;
    if (t < 1) requestAnimationFrame(tick); else done();
  };
  requestAnimationFrame(tick);
}

function revealSection(container) {
  revealedSections.add(container.id);
  container.querySelectorAll(".infographic").forEach((img) => img.classList.add("is-in"));
  container.querySelectorAll("[data-count]").forEach(animateCount);
  container.querySelectorAll(".bar-fill[data-w]").forEach((bar, i) => {
    bar.style.transitionDelay = reduceMotion ? "0ms" : `${Math.min(i * 60, 420)}ms`;
    bar.style.width = `${bar.dataset.w}%`;
  });
  container.querySelectorAll(".heat").forEach((cell, i) => {
    cell.style.transitionDelay = reduceMotion ? "0ms" : `${Math.min(i * 14, 600)}ms`;
    cell.classList.add("is-in");
  });
}

const sectionObserver = ("IntersectionObserver" in window && !reduceMotion)
  ? new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        sectionObserver.unobserve(entry.target);
        revealSection(entry.target);
      });
    }, { threshold: 0.2 })
  : null;

function armSection(container) {
  if (!container || revealedSections.has(container.id)) return;
  if (!sectionObserver) { revealSection(container); return; }
  sectionObserver.observe(container);
}

function initScrollEffects() {
  // One passive rAF handler drives both: the reading-progress hairline and a
  // slow editorial drift on the hero figure (depth, not decoration). The drift
  // is desktop-only; mobile scroll keeps its own physics.
  const progress = byId("scrollProgress");
  const figure = document.querySelector(".hero-figure");
  const drift = !reduceMotion && window.matchMedia("(min-width: 60rem)").matches;
  if (reduceMotion) return;
  let ticking = false;
  const apply = () => {
    ticking = false;
    const max = document.documentElement.scrollHeight - window.innerHeight;
    if (progress && max > 0) progress.style.transform = `scaleX(${Math.min(window.scrollY / max, 1)})`;
    if (figure && drift) {
      const yv = Math.min(window.scrollY, 820);
      figure.style.transform = `translateY(${(yv * 0.22).toFixed(1)}px)`;
      figure.style.opacity = Math.max(1 - yv / 760, 0).toFixed(3);
    }
  };
  window.addEventListener("scroll", () => {
    if (!ticking) { ticking = true; requestAnimationFrame(apply); }
  }, { passive: true });
  apply();
}

function init() {
  byId("dataCommit").textContent = data.meta.data_commit.slice(0, 7);
  renderHeroFigure();
  renderMetrics();
  buildControls();
  renderAll();
  armSection(byId("infographic"));
  initScrollEffects();
  byId("questionSearch").addEventListener("input", (event) => {
    state.query = event.target.value.trim().toLowerCase();
    renderQuestions();
  });
  byId("copyCitation").addEventListener("click", async () => {
    const text = byId("citationText").textContent;
    await navigator.clipboard.writeText(text);
    byId("copyCitation").textContent = "Copied";
    setTimeout(() => { byId("copyCitation").textContent = "Copy BibTeX"; }, 1400);
  });
}

function renderHeroFigure() {
  // Stat-Led hero reveal: tick the figure from 0 to the live top score (~500 ms).
  const el = byId("heroFigure");
  const target = defaultModel()?.accuracy ?? parseFloat(el.dataset.target);
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    el.textContent = target.toFixed(1);
    return;
  }
  const start = performance.now();
  const dur = 500;
  const tick = (now) => {
    const t = Math.min((now - start) / dur, 1);
    el.textContent = (target * (1 - Math.pow(1 - t, 3))).toFixed(1);
    if (t < 1) requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}

function renderMetrics() {
  const judgeVerdicts = data.overall.rows + data.judge_agreement.reduce((sum, judge) => sum + judge.paired, 0);
  const items = [
    [data.overall.models, "frontier models"],
    [data.overall.questions, "clinician-reviewed questions"],
    [judgeVerdicts, "judge verdicts recorded"],
    [data.overall.refusals, "refusals, all labeled"],
  ];
  byId("metricGrid").innerHTML = items.map(([value, label]) => `
    <div class="metric">
      <strong data-count="${value}">0</strong>
      <span>${label}</span>
    </div>
  `).join("");
  armSection(byId("metricGrid"));
}

function buildControls() {
  const domainOptions = [
    ["all", "All domains"],
    ...data.domains.map((domain) => [domain.id, domain.label]),
  ];
  const tierOptions = [
    ["all", "All tiers"],
    ...Array.from(new Set(data.models.map((model) => model.tier))).sort().map((tier) => [tier, titleCase(tier)]),
  ];
  const providerOptions = [
    ["all", "All providers"],
    ...Array.from(new Set(data.models.map((model) => model.provider))).sort().map((provider) => [provider, provider]),
  ];
  populateSelect("domainFilter", domainOptions, "domain");
  populateSelect("tierFilter", tierOptions, "tier");
  populateSelect("providerFilter", providerOptions, "provider");
}

function populateSelect(id, options, key) {
  const select = byId(id);
  select.innerHTML = options.map(([value, label]) => `<option value="${escapeHtml(value)}">${escapeHtml(label)}</option>`).join("");
  select.addEventListener("change", (event) => {
    state[key] = event.target.value;
    renderAll();
  });
}

function titleCase(value) {
  return value ? value[0].toUpperCase() + value.slice(1) : value;
}

function filteredModels() {
  return data.models
    .filter((model) => state.tier === "all" || model.tier === state.tier)
    .filter((model) => state.provider === "all" || model.provider === state.provider)
    .map((model) => {
      if (state.domain === "all") return { ...model, viewAccuracy: model.accuracy, viewCorrect: model.correct, viewTotal: model.total };
      const domain = model.domains[state.domain] || { accuracy: 0, correct: 0, total: 0 };
      return { ...model, viewAccuracy: domain.accuracy, viewCorrect: domain.correct, viewTotal: domain.total };
    })
    .sort((a, b) => b.viewAccuracy - a.viewAccuracy || b.answered_accuracy - a.answered_accuracy);
}

function renderAll() {
  if (!state.selectedModel || !data.models.some((model) => model.model === state.selectedModel)) {
    state.selectedModel = defaultModel()?.model;
  }
  renderLeaderboard();
  renderModelDetail();
  renderMatrix();
  renderQuestions();
  renderErrors();
  renderJudges();
}

function defaultModel() {
  return [...data.models].sort((a, b) => b.accuracy - a.accuracy || b.answered_accuracy - a.answered_accuracy)[0];
}

function renderLeaderboard() {
  const rows = filteredModels();
  if (!rows.some((model) => model.model === state.selectedModel)) {
    state.selectedModel = rows[0]?.model || data.models[0]?.model;
  }
  byId("leaderboardRows").innerHTML = rows.map((model) => `
    <button class="leader-row ${model.model === state.selectedModel ? "is-active" : ""}" type="button" data-model="${escapeHtml(model.model)}">
      <span class="model-name">
        <img class="logo" src="${escapeHtml(model.logo)}" alt="${escapeHtml(model.provider)} logo">
        <span>
          <strong>${escapeHtml(model.model)}</strong>
          <span>${escapeHtml(model.provider)} · ${escapeHtml(titleCase(model.tier))}</span>
        </span>
      </span>
      <span class="bar-track" aria-hidden="true">
        <span class="bar-fill" data-w="${model.viewAccuracy}" style="width:${revealedSections.has("leaderboardRows") ? model.viewAccuracy : 0}%; background:${model.color}"></span>
      </span>
      <span class="score">
        <strong>${fmtPct(model.viewAccuracy)}</strong>
        <span>${model.viewCorrect}/${model.viewTotal}</span>
      </span>
    </button>
  `).join("");
  document.querySelectorAll(".leader-row").forEach((row) => {
    row.addEventListener("click", () => {
      state.selectedModel = row.dataset.model;
      renderLeaderboard();
      renderModelDetail();
    });
  });
  armSection(byId("leaderboardRows"));
}

function selectedModel() {
  return data.models.find((model) => model.model === state.selectedModel) || data.models[0];
}

function renderModelDetail() {
  const model = selectedModel();
  const refusalText = model.refusals.length ? model.refusals.join(", ") : "none";
  byId("modelDetail").innerHTML = `
    <div class="model-name">
      <img class="logo" src="${escapeHtml(model.logo)}" alt="${escapeHtml(model.provider)} logo">
      <span>
        <strong>${escapeHtml(model.model)}</strong>
        <span>${escapeHtml(model.model_id)}</span>
      </span>
    </div>
    <div class="detail-list">
      <div><span>Deployment accuracy</span><strong>${fmtPct(model.accuracy)} (${model.correct}/${model.total})</strong></div>
      <div><span>Bootstrap interval</span><strong>${model.ci_low.toFixed(1)}–${model.ci_high.toFixed(1)}%</strong></div>
      <div><span>Answer rate</span><strong>${fmtPct(model.answer_rate)}</strong></div>
      <div><span>Accuracy on answered</span><strong>${fmtPct(model.answered_accuracy)}</strong></div>
      <div><span>Mean latency</span><strong>${model.latency.toFixed(1)} s</strong></div>
      <div><span>Refusals</span><strong>${escapeHtml(refusalText)}</strong></div>
    </div>
  `;
}

function renderMatrix() {
  const headers = data.domains.map((domain) => `<th>${escapeHtml(domain.label)}</th>`).join("");
  const revealed = revealedSections.has("domainMatrix");
  const rows = data.models.map((model) => {
    const cells = data.domains.map((domain) => {
      const cell = model.domains[domain.id];
      const color = heatColor(cell.accuracy);
      return `<td><span class="heat ${revealed ? "is-in" : ""}" style="display:block; padding:9px; background:${color}">${cell.accuracy.toFixed(0)}</span></td>`;
    }).join("");
    return `
      <tr>
        <td><span class="model-name"><img class="logo" src="${escapeHtml(model.logo)}" alt=""><strong>${escapeHtml(model.model)}</strong></span></td>
        ${cells}
      </tr>
    `;
  }).join("");
  byId("domainMatrix").innerHTML = `
    <table class="matrix">
      <thead><tr><th>Model</th>${headers}</tr></thead>
      <tbody>${rows}</tbody>
    </table>
  `;
  armSection(byId("domainMatrix"));
}

// Functional data ramp mirroring tokens.css --color-ok / --color-warn / --color-bad.
function heatColor(value) {
  if (value >= 90) return "#2e7d6f";
  if (value >= 75) return "#5a9a8a";
  if (value >= 60) return "#bd8d3c";
  if (value >= 40) return "#c2703f";
  return "#b14a3a";
}

function renderQuestions() {
  const selectedDomain = state.domain;
  const query = state.query;
  const questions = data.questions
    .filter((question) => selectedDomain === "all" || question.domain === selectedDomain)
    .filter((question) => !query || (question.search_text || `${question.id} ${question.question} ${question.domain_label}`).toLowerCase().includes(query));

  byId("questionGrid").innerHTML = questions.map((question) => `
    <article class="question-card">
      <div class="chips">
        <span class="chip">${escapeHtml(question.id)}</span>
        <span class="chip">${escapeHtml(question.domain_label)}</span>
        <span class="chip">${escapeHtml(question.difficulty)}</span>
        <span class="chip">${question.correct}/${question.total} correct</span>
      </div>
      <p>${escapeHtml(question.question)}</p>
      <div class="outcome-dots" aria-label="Model outcomes">
        ${question.outcomes.map((outcome) => `
          <span
            class="dot ${outcomeClass(outcome)}"
            title="${escapeHtml(outcome.model)}: ${outcome.correct ? "correct" : outcome.answered ? "incorrect" : "refusal"}"
            aria-label="${escapeHtml(outcome.model)} ${outcome.correct ? "correct" : outcome.answered ? "incorrect" : "refusal"}"></span>
        `).join("")}
      </div>
    </article>
  `).join("");
}

function outcomeClass(outcome) {
  if (!outcome.answered) return "refusal";
  return outcome.correct ? "correct" : "wrong";
}

function renderErrors() {
  const maxRows = Math.max(...data.error_analysis.categories.map((category) => category.rows));
  byId("errorCategories").innerHTML = data.error_analysis.categories.map((category) => `
    <div class="error-item">
      <div class="error-count" data-count="${category.rows}">0</div>
      <div>
        <strong>${escapeHtml(category.name)}</strong>
        <p>${escapeHtml(category.summary)}</p>
        <div class="bar-track" aria-hidden="true">
          <div class="bar-fill" data-w="${(category.rows / maxRows) * 100}" style="width:0%; background:#2e7d6f"></div>
        </div>
      </div>
    </div>
  `).join("");
  armSection(byId("errorCategories"));

  byId("judgeFlags").innerHTML = data.error_analysis.internal_candidates.map((flag) => `
    <div class="flag-row">
      <span><strong>${escapeHtml(flag.model)}</strong><br><span class="muted">${escapeHtml(flag.qid)} · ${escapeHtml(flag.domain)}</span></span>
      <span class="chip">GPT-5.2 ${flag.gpt52 ? "correct" : "incorrect"} · GPT-5.5 ${flag.gpt55 ? "correct" : "incorrect"}</span>
    </div>
  `).join("");
}

function renderJudges() {
  byId("judgeCards").innerHTML = data.judge_agreement.map((judge) => `
    <div class="judge-card">
      <span class="chip">${escapeHtml(judge.judge)}</span>
      <strong data-count="${judge.agreement.toFixed(1)}" data-decimals="1" data-suffix="%">0%</strong>
      <span>${judge.paired} paired answered rows; Cohen's kappa ${judge.kappa.toFixed(3)}</span>
    </div>
  `).join("");
  armSection(byId("judgeCards"));

  const judges = data.judge_agreement;
  const models = data.models.map((model) => model.model);
  const rows = models.map((model) => {
    const cells = judges.map((judge) => {
      const row = judge.per_model.find((entry) => entry.model === model);
      return `<td>${row ? `${row.secondary_accuracy.toFixed(1)}%` : "-"}</td>`;
    }).join("");
    return `<tr><td>${escapeHtml(model)}</td><td>${data.models.find((m) => m.model === model).accuracy.toFixed(1)}%</td>${cells}</tr>`;
  }).join("");
  byId("judgeTable").innerHTML = `
    <table class="judge-table">
      <thead><tr><th>Model</th><th>Primary judge</th>${judges.map((judge) => `<th>${escapeHtml(judge.judge.replace("openai/", ""))}</th>`).join("")}</tr></thead>
      <tbody>${rows}</tbody>
    </table>
  `;
}

init();
