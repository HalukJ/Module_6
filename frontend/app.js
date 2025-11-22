const featureMatrix = [
  { key: "consoleAccess", label: "Console library" },
  { key: "pcAccess", label: "PC library" },
  { key: "cloudGaming", label: "Cloud gaming & streaming" },
  { key: "eaPlay", label: "EA Play included" },
  { key: "dayOne", label: "Day-one releases" },
  { key: "onlineMultiplayer", label: "Online multiplayer" },
  { key: "memberDiscounts", label: "Member discounts & quests" },
];

const chartColors = ["#3fe077", "#73ff85", "#32b561"];

const fallbackPlanPayload = {
  order: ["Core", "PC", "Ultimate"],
  plans: {
    Core: {
      name: "Core",
      price: 9.99,
      tagline: "Essential console multiplayer",
      description: "Console multiplayer, rotating library",
      best_for: "Players who live on Xbox and host couch co-op nights.",
      devices: ["Xbox Series X|S", "Xbox One"],
      hours_range: [8, 30],
      perks: ["Xbox Live access", "Member deals", "Console catalog"],
      features: {
        consoleAccess: true,
        pcAccess: false,
        cloudGaming: false,
        eaPlay: false,
        dayOne: true,
        onlineMultiplayer: true,
        memberDiscounts: true,
      },
    },
    PC: {
      name: "PC",
      price: 10.99,
      tagline: "Unlimited PC library",
      description: "Large PC catalog + EA Play",
      best_for: "Mouse and keyboard tacticians who mod everything.",
      devices: ["Windows PC"],
      hours_range: [15, 45],
      perks: ["EA Play on PC", "Member deals", "PC catalog"],
      features: {
        consoleAccess: false,
        pcAccess: true,
        cloudGaming: false,
        eaPlay: true,
        dayOne: true,
        onlineMultiplayer: true,
        memberDiscounts: true,
      },
    },
    Ultimate: {
      name: "Ultimate",
      price: 16.99,
      tagline: "All devices. All perks.",
      description: "Console, PC and cloud streaming",
      best_for: "Players hopping between screens and streaming everywhere.",
      devices: ["Xbox", "PC", "Cloud"],
      hours_range: [25, 70],
      perks: ["Cloud streaming", "EA Play everywhere", "Day-one releases", "Ultimate rewards"],
      features: {
        consoleAccess: true,
        pcAccess: true,
        cloudGaming: true,
        eaPlay: true,
        dayOne: true,
        onlineMultiplayer: true,
        memberDiscounts: true,
      },
    },
  },
};

const fallbackSummary = {
  Core: { count: 400, avg_hours: 18, top_genres: ["Shooter", "Sports"], top_devices: ["Xbox"] },
  PC: {
    count: 330,
    avg_hours: 27,
    top_genres: ["Strategy", "RPG"],
    top_devices: ["Windows PC"],
  },
  Ultimate: {
    count: 270,
    avg_hours: 38,
    top_genres: ["Action Adventure", "Shooter"],
    top_devices: ["Xbox", "Cloud"],
  },
};

let planData = {};
let planOrder = [];
let userSummary = {};
let totalMembers = 0;
let selectedPlanKey = null;
let apiAvailable = true;

const planGrid = document.querySelector("#planGrid");
const planSelect = document.querySelector("#planSelect");
const differenceList = document.querySelector("#differenceList");
const selectedPlanName = document.querySelector("#selectedPlanName");
const selectedPlanTagline = document.querySelector("#selectedPlanTagline");
const selectedPlanPrice = document.querySelector("#selectedPlanPrice");
const selectedPlanPerks = document.querySelector("#selectedPlanPerks");
const selectedPlanStats = document.querySelector("#selectedPlanStats");
const selectedPlanMembers = document.querySelector("#selectedPlanMembers");
const communityStats = document.querySelector("#communityStats");
const comparisonTableBody = document.querySelector("#comparisonTable tbody");
const experienceSection = document.querySelector("#experience");
const experienceWelcome = document.querySelector("#experienceWelcome");
const experienceCopy = document.querySelector("#experienceCopy");
const experienceActions = document.querySelector("#experienceActions");
const experienceCapabilities = document.querySelector("#experienceCapabilities");
const planChartCanvas = document.querySelector("#planChart");
const analyticsTableBody = document.querySelector("#analyticsTableBody");
const analyticsTotal = document.querySelector("#analyticsTotal");
const subscribeForm = document.querySelector("#subscribeForm");
const subscribeNameInput = document.querySelector("#subscribeName");
const subscribeButton = document.querySelector("#subscribeButton");
const subscribeStatus = document.querySelector("#subscribeStatus");

async function fetchJSON(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json();
}

function setPlanData(payload) {
  planData = payload.plans;
  planOrder = payload.order;
}

function renderPlanGrid() {
  planGrid.innerHTML = "";
  planOrder.forEach((key) => {
    const plan = planData[key];
    const card = document.createElement("article");
    card.className = "plan-card";
    card.dataset.plan = key;
    card.innerHTML = `
      <p class="eyebrow">${plan.tagline}</p>
      <h3>${plan.name}</h3>
      <p>${plan.description}</p>
      <div class="plan-card__price">$${plan.price.toFixed(2)}<span>/month</span></div>
      <ul>
        <li>Best for: ${plan.best_for}</li>
        <li>Devices: ${plan.devices.join(", ")}</li>
        <li>Typical playtime: ${plan.hours_range[0]}-${plan.hours_range[1]} hrs/month</li>
      </ul>
      <button class="cta primary" data-plan-select="${key}">Choose ${plan.name}</button>
    `;
    planGrid.appendChild(card);
  });
}

function populateSelect() {
  planSelect.innerHTML = "";
  planOrder.forEach((key) => {
    const plan = planData[key];
    const option = document.createElement("option");
    option.value = key;
    option.textContent = `${plan.name} - $${plan.price.toFixed(2)}/mo`;
    planSelect.appendChild(option);
  });
}

function renderComparisonTable() {
  comparisonTableBody.innerHTML = "";
  featureMatrix.forEach((feature) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <th scope="row">${feature.label}</th>
      ${planOrder
        .map((plan) => {
          const value = planData[plan].features[feature.key];
          return `<td data-value="${value}">${value ? "Included" : "—"}</td>`;
        })
        .join("")}
    `;
    comparisonTableBody.appendChild(row);
  });
}

function computeDifferences(planKey) {
  const plan = planData[planKey];
  const others = planOrder.filter((key) => key !== planKey);
  const diffs = [];

  featureMatrix.forEach((feature) => {
    const hasFeature = plan.features[feature.key];
    if (!hasFeature) return;
    const missingElsewhere = others.filter((key) => !planData[key].features[feature.key]);
    if (missingElsewhere.length) {
      diffs.push(`${feature.label} (absent from ${missingElsewhere.join(" & ")})`);
    }
  });

  const uniquePerks = plan.perks.filter((perk) =>
    others.every((other) => !planData[other].perks.includes(perk))
  );
  uniquePerks.forEach((perk) => diffs.push(`Exclusive perk: ${perk}`));

  const avgHours = (plan.hours_range[0] + plan.hours_range[1]) / 2;
  const otherAverage =
    others.reduce((total, key) => {
      const [low, high] = planData[key].hours_range;
      return total + (low + high) / 2;
    }, 0) / others.length;
  if (avgHours > otherAverage + 5) {
    diffs.push("Built for marathon sessions and heavy users.");
  } else if (avgHours < otherAverage - 5) {
    diffs.push("Perfect for casual or social sessions.");
  }

  if (!diffs.length) {
    diffs.push("Shares the core MUDTPass benefits across all plans.");
  }

  return diffs;
}

function renderCommunityStats() {
  if (!communityStats) return;
  communityStats.innerHTML = planOrder
    .map((plan) => {
      const stats = userSummary[plan];
      const count = stats ? stats.count : 0;
      const avgHours = stats ? stats.avg_hours : 0;
      const percent = totalMembers ? ((count / totalMembers) * 100).toFixed(1) : "0.0";
      return `<li><strong>${plan}</strong>: ${count} members · ${avgHours} avg hrs/mo · ${percent}% of total</li>`;
    })
    .join("");
}

function setSubscribeStatus(text, state = "info") {
  if (!subscribeStatus) return;
  subscribeStatus.textContent = text;
  subscribeStatus.classList.remove("status-success", "status-error", "status-info");
  subscribeStatus.classList.add(`status-${state}`);
}

function renderStats(planKey) {
  const stats = userSummary[planKey];
  if (!stats) {
    selectedPlanStats.innerHTML = "<span>No data available yet.</span>";
    return;
  }

  const genres = stats.top_genres.length ? stats.top_genres.join(", ") : "—";
  const devices = stats.top_devices.length ? stats.top_devices.join(", ") : "—";
  selectedPlanStats.innerHTML = `
    <span>Members: ${stats.count.toLocaleString()}</span>
    <span>Average hours/month: ${stats.avg_hours}</span>
    <span>Top genres: ${genres}</span>
    <span>Preferred devices: ${devices}</span>
  `;
}

function renderExperience(planKey) {
  if (!experienceSection) return;
  const plan = planData[planKey];
  if (!plan) return;
  experienceSection.classList.remove("hidden");
  updateSubscribeUI();

  const stats = userSummary[planKey];
  const memberCount = stats ? stats.count.toLocaleString() : "hundreds of";
  const avgHours = stats ? `${stats.avg_hours} hrs/month` : "fresh sessions every week";
  const genres = stats && stats.top_genres.length ? stats.top_genres.join(", ") : "mixed genres";
  const perksPreview = plan.perks.slice(0, 2).join(" & ") || "exclusive launch titles";

  experienceWelcome.textContent = `Welcome to the ${plan.name} community`;
  experienceCopy.textContent = `You now stand alongside ${memberCount} MUDTPass players. ${plan.best_for}`;
  experienceActions.innerHTML = [
    `Jump into ${plan.devices.join(", ")} immediately.`,
    `Average playtime: ${avgHours}.`,
    `Popular genres here: ${genres}.`,
    `Claim perks such as ${perksPreview}.`,
  ]
    .map((item) => `<li class="enabled">${item}</li>`)
    .join("");

  experienceCapabilities.innerHTML = featureMatrix
    .map((feature) => {
      const enabled = !!plan.features[feature.key];
      const label = `${feature.label}: ${enabled ? "Included" : "Locked"}`;
      return `<li class="${enabled ? "enabled" : "disabled"}">${label}</li>`;
    })
    .join("");
}

function updateSubscribeUI() {
  if (!subscribeButton || !subscribeNameInput || !planData) return;
  if (!apiAvailable) {
    subscribeButton.disabled = true;
    setSubscribeStatus("Start the backend server to enable subscriptions.", "error");
    return;
  }

  if (!selectedPlanKey) {
    subscribeButton.disabled = true;
    setSubscribeStatus("Pick a plan to enable subscriptions.", "info");
    return;
  }

  subscribeButton.disabled = false;
  subscribeButton.textContent = `Subscribe to ${planData[selectedPlanKey].name}`;
  setSubscribeStatus("Enter your gamer name to join instantly.", "info");
}

function renderAnalyticsTable() {
  if (!analyticsTableBody) return;
  analyticsTableBody.innerHTML = planOrder
    .map((plan) => {
      const stats = userSummary[plan] || { count: 0 };
      const count = stats.count || 0;
      const percent = totalMembers ? ((count / totalMembers) * 100).toFixed(1) : "0.0";
      return `<tr>
        <td>${plan}</td>
        <td>${count.toLocaleString()}</td>
        <td>${percent}%</td>
      </tr>`;
    })
    .join("");

  if (analyticsTotal) {
    analyticsTotal.textContent = totalMembers.toLocaleString();
  }
}

function renderPlanChart() {
  if (!planChartCanvas || !planChartCanvas.getContext) return;
  const ctx = planChartCanvas.getContext("2d");
  const width = planChartCanvas.width;
  const height = planChartCanvas.height;
  ctx.clearRect(0, 0, width, height);

  if (!totalMembers) {
    ctx.fillStyle = "#9ba7b4";
    ctx.font = "500 16px 'Space Grotesk', sans-serif";
    ctx.fillText("Start the backend to visualize live stats.", 20, height / 2);
    return;
  }

  const barHeight = 40;
  const gap = 20;
  const maxBarWidth = width - 150;
  const chartHeight = planOrder.length * (barHeight + gap) - gap;
  const offsetY = Math.max((height - chartHeight) / 2, 10);

  planOrder.forEach((plan, index) => {
    const stats = userSummary[plan] || { count: 0 };
    const percent = totalMembers ? stats.count / totalMembers : 0;
    const barWidth = Math.max(percent * maxBarWidth, 2);
    const y = offsetY + index * (barHeight + gap);

    ctx.fillStyle = "rgba(255, 255, 255, 0.08)";
    ctx.fillRect(120, y, maxBarWidth, barHeight);

    ctx.fillStyle = chartColors[index % chartColors.length];
    ctx.fillRect(120, y, barWidth, barHeight);

    ctx.fillStyle = "#f5f8fa";
    ctx.font = "600 16px 'Space Grotesk', sans-serif";
    ctx.fillText(plan, 20, y + barHeight / 2 + 6);

    ctx.font = "500 14px 'Space Grotesk', sans-serif";
    ctx.fillText(`${(percent * 100).toFixed(1)}%`, 130 + barWidth, y + barHeight / 2 + 6);
  });
}

function renderAnalytics() {
  totalMembers = planOrder.reduce(
    (total, plan) => total + (userSummary[plan] ? userSummary[plan].count : 0),
    0
  );
  renderCommunityStats();
  renderAnalyticsTable();
  renderPlanChart();
}

async function handleSubscribe(event) {
  event.preventDefault();
  if (!apiAvailable) {
    setSubscribeStatus("Backend is offline. Start server.py first.", "error");
    return;
  }
  if (!selectedPlanKey) {
    setSubscribeStatus("Select a plan before subscribing.", "error");
    return;
  }
  const name = subscribeNameInput.value.trim();
  if (!name) {
    setSubscribeStatus("Please enter your name.", "error");
    return;
  }

  subscribeButton.disabled = true;
  setSubscribeStatus("Processing your subscription...", "info");
  try {
    const response = await fetch("/api/subscribe", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, plan: selectedPlanKey }),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Subscription failed.");
    }
    subscribeNameInput.value = "";
    setSubscribeStatus(
      `Welcome, ${data.user.full_name}! You're now part of ${data.plan}.`,
      "success"
    );
    userSummary = data.summary;
    renderAnalytics();
    renderStats(selectedPlanKey);
    fetchPlanMembers(selectedPlanKey);
  } catch (error) {
    setSubscribeStatus(error.message || "Unable to subscribe right now.", "error");
  } finally {
    subscribeButton.disabled = false;
  }
}

async function fetchPlanMembers(planKey) {
  selectedPlanMembers.innerHTML = "<li>Loading players...</li>";
  try {
    const payload = await fetchJSON(`/api/users/${encodeURIComponent(planKey)}?limit=6`);
    if (!payload.users.length) {
      selectedPlanMembers.innerHTML = "<li>No members recorded yet.</li>";
      return;
    }
    selectedPlanMembers.innerHTML = payload.users
      .map(
        (user) => `
        <li>
          <strong>${user.full_name}</strong> · ${user.favorite_genre}<br />
          ${user.preferred_device} · ${user.hours_per_month} hrs/mo
        </li>
      `
      )
      .join("");
  } catch (error) {
    selectedPlanMembers.innerHTML =
      "<li>Unable to load members. Start the backend to view live data.</li>";
  }
}

function selectPlan(planKey) {
  const plan = planData[planKey];
  selectedPlanKey = planKey;
  planSelect.value = planKey;
  selectedPlanName.textContent = `${plan.name} membership`;
  selectedPlanTagline.textContent = `${plan.tagline} · ${plan.description} ${plan.best_for}`;
  selectedPlanPrice.textContent = `$${plan.price.toFixed(2)}/month`;
  selectedPlanPerks.innerHTML = plan.perks.map((perk) => `<li>${perk}</li>`).join("");

  const diffs = computeDifferences(planKey);
  differenceList.innerHTML = diffs.map((item) => `<li>${item}</li>`).join("");
  renderStats(planKey);
  renderExperience(planKey);
  updateSubscribeUI();
  fetchPlanMembers(planKey);
}

function attachEvents() {
  planGrid.addEventListener("click", (event) => {
    const button = event.target.closest("[data-plan-select]");
    if (!button) return;
    selectPlan(button.dataset.planSelect);
    button.blur();
  });

  planSelect.addEventListener("change", (event) => {
    selectPlan(event.target.value);
  });

  if (subscribeForm) {
    subscribeForm.addEventListener("submit", handleSubscribe);
  }
}

async function init() {
  try {
    const [planPayload, summaryPayload] = await Promise.all([
      fetchJSON("/api/plans"),
      fetchJSON("/api/users/summary"),
    ]);
    setPlanData(planPayload);
    userSummary = summaryPayload;
    apiAvailable = true;
  } catch (error) {
    console.warn("Falling back to static data:", error);
    setPlanData(fallbackPlanPayload);
    userSummary = fallbackSummary;
    apiAvailable = false;
  }

  renderPlanGrid();
  populateSelect();
  renderComparisonTable();
  renderAnalytics();
  attachEvents();
  selectPlan(planOrder[0]);
  updateSubscribeUI();
}

document.addEventListener("DOMContentLoaded", init);
