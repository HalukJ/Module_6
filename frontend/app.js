const featureMatrix = [
  { key: "consoleAccess", label: "Console library" },
  { key: "pcAccess", label: "PC library" },
  { key: "cloudGaming", label: "Cloud gaming & streaming" },
  { key: "eaPlay", label: "EA Play included" },
  { key: "dayOne", label: "Day-one releases" },
  { key: "onlineMultiplayer", label: "Online multiplayer" },
  { key: "memberDiscounts", label: "Member discounts & quests" },
];

const planColors = { Core: "#3fe077", PC: "#3ba7ff", Ultimate: "#ff4d5a" };
const planCosts = { Core: 0.12, PC: 0.16, Ultimate: 0.22 };

const fallbackPlanPayload = {
  order: ["Core", "PC", "Ultimate"],
  plans: {
    Core: {
      name: "Core",
      is_favorite: false,
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
      is_favorite: false,
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
      is_favorite: true,
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

const fallbackMonthlyPerformance = {
  plan_order: ["Core", "PC", "Ultimate"],
  months: [
    {
      month: "January",
      plans: {
        Core: { users: 400, avg_hours: 18, total_hours: 7200, profit: 3996.0 },
        PC: { users: 357, avg_hours: 27, total_hours: 9639, profit: 3923.43 },
        Ultimate: { users: 227, avg_hours: 38, total_hours: 8626, profit: 3856.73 },
      },
      total_profit: 11776.16,
      total_hours: 25465,
    },
    {
      month: "February",
      plans: {
        Core: { users: 376, avg_hours: 18, total_hours: 6768, profit: 3756.24 },
        PC: { users: 347, avg_hours: 26, total_hours: 9022, profit: 3813.53 },
        Ultimate: { users: 241, avg_hours: 38, total_hours: 9158, profit: 4094.59 },
      },
      total_profit: 11664.36,
      total_hours: 24948,
    },
    {
      month: "March",
      plans: {
        Core: { users: 377, avg_hours: 17, total_hours: 6409, profit: 3766.23 },
        PC: { users: 340, avg_hours: 26, total_hours: 8840, profit: 3736.6 },
        Ultimate: { users: 225, avg_hours: 37, total_hours: 8325, profit: 3822.75 },
      },
      total_profit: 11325.58,
      total_hours: 23574,
    },
    {
      month: "April",
      plans: {
        Core: { users: 362, avg_hours: 17, total_hours: 6154, profit: 3616.38 },
        PC: { users: 326, avg_hours: 25, total_hours: 8150, profit: 3582.74 },
        Ultimate: { users: 235, avg_hours: 36, total_hours: 8460, profit: 3992.65 },
      },
      total_profit: 11191.77,
      total_hours: 22764,
    },
    {
      month: "May",
      plans: {
        Core: { users: 365, avg_hours: 17, total_hours: 6205, profit: 3646.35 },
        PC: { users: 319, avg_hours: 25, total_hours: 7975, profit: 3505.81 },
        Ultimate: { users: 224, avg_hours: 36, total_hours: 8064, profit: 3805.76 },
      },
      total_profit: 10957.92,
      total_hours: 22244,
    },
    {
      month: "June",
      plans: {
        Core: { users: 370, avg_hours: 16, total_hours: 5920, profit: 3696.3 },
        PC: { users: 296, avg_hours: 24, total_hours: 7104, profit: 3253.04 },
        Ultimate: { users: 221, avg_hours: 35, total_hours: 7735, profit: 3754.79 },
      },
      total_profit: 10704.13,
      total_hours: 20759,
    },
    {
      month: "July",
      plans: {
        Core: { users: 355, avg_hours: 16, total_hours: 5680, profit: 3546.45 },
        PC: { users: 282, avg_hours: 24, total_hours: 6768, profit: 3099.18 },
        Ultimate: { users: 237, avg_hours: 35, total_hours: 8295, profit: 4026.63 },
      },
      total_profit: 10672.26,
      total_hours: 20743,
    },
    {
      month: "August",
      plans: {
        Core: { users: 352, avg_hours: 16, total_hours: 5632, profit: 3516.48 },
        PC: { users: 272, avg_hours: 23, total_hours: 6256, profit: 2989.28 },
        Ultimate: { users: 236, avg_hours: 35, total_hours: 8260, profit: 4009.64 },
      },
      total_profit: 10515.4,
      total_hours: 20148,
    },
    {
      month: "September",
      plans: {
        Core: { users: 348, avg_hours: 15, total_hours: 5220, profit: 3476.52 },
        PC: { users: 269, avg_hours: 23, total_hours: 6187, profit: 2956.31 },
        Ultimate: { users: 223, avg_hours: 34, total_hours: 7582, profit: 3788.77 },
      },
      total_profit: 10221.6,
      total_hours: 18989,
    },
    {
      month: "October",
      plans: {
        Core: { users: 340, avg_hours: 15, total_hours: 5100, profit: 3396.6 },
        PC: { users: 264, avg_hours: 22, total_hours: 5808, profit: 2901.36 },
        Ultimate: { users: 221, avg_hours: 34, total_hours: 7514, profit: 3754.79 },
      },
      total_profit: 10052.75,
      total_hours: 18422,
    },
    {
      month: "November",
      plans: {
        Core: { users: 327, avg_hours: 15, total_hours: 4905, profit: 3266.73 },
        PC: { users: 272, avg_hours: 22, total_hours: 5984, profit: 2989.28 },
        Ultimate: { users: 209, avg_hours: 33, total_hours: 6897, profit: 3550.91 },
      },
      total_profit: 9806.92,
      total_hours: 17786,
    },
    {
      month: "December",
      plans: {
        Core: { users: 311, avg_hours: 14, total_hours: 4354, profit: 3106.89 },
        PC: { users: 273, avg_hours: 22, total_hours: 6006, profit: 3000.27 },
        Ultimate: { users: 210, avg_hours: 33, total_hours: 6930, profit: 3567.9 },
      },
      total_profit: 9675.06,
      total_hours: 17290,
    },
  ],
};

let planData = {};
let planOrder = [];
let userSummary = {};
let totalMembers = 0;
let selectedPlanKey = null;
let apiAvailable = true;
let favoritePlanKey = null;
let monthlyPerformance = null;

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
const hoursChartCanvas = document.querySelector("#hoursChart");
const analyticsTableBody = document.querySelector("#analyticsTableBody");
const analyticsTotal = document.querySelector("#analyticsTotal");
const profitChartCanvas = document.querySelector("#profitChart");
const profitLegend = document.querySelector("#profitLegend");
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
  planData = payload.plans || {};
  planOrder = payload.order || Object.keys(planData);
  favoritePlanKey =
    planOrder.find((key) => planData[key] && planData[key].is_favorite) || null;
}

function applyCostModel(performance) {
  if (!performance?.months) return performance;
  performance.months.forEach((month) => {
    let totalProfit = 0;
    let totalHours = 0;
    Object.entries(month.plans || {}).forEach(([plan, data]) => {
      const hours = data.total_hours || 0;
      const users = data.users || 0;
      const price = planData[plan]?.price || data.price || 0;
      const revenue = users * price;
      const costRate = planCosts[plan] ?? 0.15;
      const cost = hours * costRate;
      const profit = Math.max(revenue - cost, 0);
      data.profit = Number(profit.toFixed(2));
      if (!data.avg_hours && users) {
        data.avg_hours = Number((hours / users).toFixed(1));
      }
      totalProfit += data.profit;
      totalHours += hours;
    });
    month.total_profit = Number(totalProfit.toFixed(2));
    month.total_hours = totalHours;
  });
  return performance;
}

function syncFavoriteFromPurchases() {
  if (!planOrder.length) return null;
  let topPlan = null;
  let topCount = -1;

  planOrder.forEach((plan) => {
    const count = userSummary[plan]?.count || 0;
    if (count > topCount) {
      topPlan = plan;
      topCount = count;
    }
  });

  if (!topPlan) return null;
  favoritePlanKey = topPlan;
  Object.keys(planData).forEach((plan) => {
    if (planData[plan]) {
      planData[plan].is_favorite = plan === topPlan;
    }
  });
  return topPlan;
}

function renderPlanGrid() {
  planGrid.innerHTML = "";
  planOrder.forEach((key) => {
    const plan = planData[key];
    const isFavorite = !!plan.is_favorite;
    const favoriteLabel = isFavorite ? '<span class="favorite-chip">Most popular</span>' : "";
    const card = document.createElement("article");
    card.className = `plan-card${isFavorite ? " favorite" : ""}`;
    card.dataset.plan = key;
    card.innerHTML = `
      <div class="plan-card__header">
        <p class="eyebrow">${plan.tagline}</p>
        ${favoriteLabel}
      </div>
      <h3>${plan.name}</h3>
      <p class="plan-card__desc">${plan.description}</p>
      <div class="plan-card__price">$${plan.price.toFixed(2)}<span>/month</span></div>
      <ul>
        <li>Best for: ${plan.best_for}</li>
        <li>Devices: ${plan.devices.join(", ")}</li>
        <li>Typical playtime: ${plan.hours_range[0]}-${plan.hours_range[1]} hrs/month</li>
      </ul>
      <div class="plan-card__footer">
        <button class="cta primary" data-plan-select="${key}">Choose plan</button>
      </div>
    `;
    planGrid.appendChild(card);
  });
}

function populateSelect() {
  planSelect.innerHTML = "";
  planOrder.forEach((key) => {
    const plan = planData[key];
    const favoriteSuffix = plan.is_favorite ? " *" : "";
    const option = document.createElement("option");
    option.value = key;
    option.textContent = `${plan.name} - $${plan.price.toFixed(2)}/mo${favoriteSuffix}`;
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
          const value = planData[plan]?.features?.[feature.key];
          return `<td data-value="${value}">${value ? "Included" : "Not included"}</td>`;
        })
        .join("")}
    `;
    comparisonTableBody.appendChild(row);
  });
}

function computeDifferences(planKey) {
  const plan = planData[planKey];
  if (!plan) return [];
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
      return `<li><strong>${plan}</strong>: ${count} members - ${avgHours} avg hrs/mo - ${percent}% of total</li>`;
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

  const genres = stats.top_genres.length ? stats.top_genres.join(", ") : "N/A";
  const devices = stats.top_devices.length ? stats.top_devices.join(", ") : "N/A";
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

  const barHeight = 60;
  const gap = 30;
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

    ctx.fillStyle = planColors[plan] || "#9ba7b4";
    ctx.fillRect(120, y, barWidth, barHeight);

    ctx.fillStyle = "#f5f8fa";
    ctx.font = "800 22px 'Space Grotesk', sans-serif";
    ctx.fillText(plan, 20, y + barHeight / 2 + 8);

    ctx.font = "700 20px 'Space Grotesk', sans-serif";
    ctx.fillText(`${(percent * 100).toFixed(1)}%`, 140 + barWidth, y + barHeight / 2 + 8);
  });
}

function renderHoursChart() {
  if (!hoursChartCanvas || !hoursChartCanvas.getContext) return;
  const ctx = hoursChartCanvas.getContext("2d");
  const width = hoursChartCanvas.width;
  const height = hoursChartCanvas.height;
  ctx.clearRect(0, 0, width, height);

  if (!totalMembers) {
    ctx.fillStyle = "#9ba7b4";
    ctx.font = "500 16px 'Space Grotesk', sans-serif";
    ctx.fillText("Start the backend to plot playtime hours.", 20, height / 2);
    return;
  }

  const rows = planOrder.map((plan) => {
    const stats = userSummary[plan] || { count: 0, avg_hours: 0 };
    const count = stats.count || 0;
    const avg = stats.avg_hours || 0;
    const hours = Math.round(count * avg);
    return { plan, count, avg, hours };
  });

  const rawMaxHours = Math.max(...rows.map((row) => row.hours), 1);
  const yStep = rawMaxHours > 4000 ? 2000 : rawMaxHours > 2000 ? 1000 : 500;
  const maxHours = Math.ceil(rawMaxHours / yStep) * yStep;
  const padding = 70;
  const plotWidth = width - padding * 2;
  const plotHeight = height - padding * 2;
  const barWidth = Math.min(200, Math.max(80, plotWidth / Math.max(rows.length, 1) - 40));
  const spacing = (plotWidth - rows.length * barWidth) / Math.max(rows.length + 1, 2);

  // Axes
  ctx.strokeStyle = "rgba(255, 255, 255, 0.18)";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(padding, padding);
  ctx.lineTo(padding, padding + plotHeight);
  ctx.lineTo(padding + plotWidth, padding + plotHeight);
  ctx.stroke();

  // Horizontal guides + hour labels
  const guideLines = Math.max(2, Math.min(6, Math.floor(maxHours / yStep)));
  ctx.setLineDash([4, 6]);
  for (let i = 1; i <= guideLines; i++) {
    const yValue = maxHours - yStep * i;
    const y = padding + (1 - yValue / maxHours) * plotHeight;
    ctx.beginPath();
    ctx.moveTo(padding, y);
    ctx.lineTo(padding + plotWidth, y);
    ctx.stroke();
    const label = `${yValue.toLocaleString()} hrs`;
    ctx.fillStyle = "#f5f8fa";
    ctx.font = "700 14px 'Space Grotesk', sans-serif";
    ctx.textAlign = "right";
    ctx.fillText(label, padding - 10, y + 4);
  }
  ctx.setLineDash([]);

  rows.forEach((row, index) => {
    const x = padding + spacing * (index + 1) + barWidth * index;
    const barHeight = (row.hours / maxHours) * plotHeight;
    const y = padding + plotHeight - barHeight;

    ctx.fillStyle = planColors[row.plan] || "#9ba7b4";
    ctx.fillRect(x, y, barWidth, barHeight);

    ctx.fillStyle = "#f5f8fa";
    ctx.font = "800 18px 'Space Grotesk', sans-serif";
    ctx.textAlign = "center";
    ctx.fillText(`${row.hours.toLocaleString()} hrs`, x + barWidth / 2, y - 8);

    ctx.fillStyle = "#f5f8fa";
    ctx.font = "800 20px 'Space Grotesk', sans-serif";
    ctx.textAlign = "center";
    ctx.fillText(row.plan, x + barWidth / 2, padding + plotHeight + 32);
  });
}

function renderProfitLegend(order) {
  if (!profitLegend) return;
  profitLegend.innerHTML = order
    .map(
      (plan) => `
        <span class="legend-item">
          <span class="legend-swatch" style="background:${planColors[plan] || "#9ba7b4"}"></span>
          ${plan}
        </span>
      `
    )
    .join("");
}

function renderMonthlyProfitChart() {
  if (!profitChartCanvas || !profitChartCanvas.getContext) return;
  const ctx = profitChartCanvas.getContext("2d");
  const width = profitChartCanvas.width;
  const height = profitChartCanvas.height;
  ctx.clearRect(0, 0, width, height);

  if (!monthlyPerformance || !monthlyPerformance.months?.length) {
    ctx.fillStyle = "#9ba7b4";
    ctx.font = "500 16px 'Space Grotesk', sans-serif";
    ctx.fillText("Start the backend to simulate monthly profit.", 20, height / 2);
    return;
  }

  const monthData = monthlyPerformance.months;
  const order = monthlyPerformance.plan_order?.length
    ? monthlyPerformance.plan_order
    : planOrder;
  if (order.length) {
    renderProfitLegend(order);
  }

  const padding = 50;
  const plotWidth = width - padding * 2;
  const plotHeight = height - padding * 2;

  const profitValues = monthData.flatMap((month) =>
    order.map((plan) => month.plans?.[plan]?.profit || 0)
  );
  const rawMaxProfit = Math.max(...profitValues, 1);
  const profitStep =
    rawMaxProfit > 20000 ? 5000 : rawMaxProfit > 10000 ? 2000 : rawMaxProfit > 5000 ? 1000 : 500;
  const maxProfit = Math.ceil(rawMaxProfit / profitStep) * profitStep;
  const xStep = plotWidth / Math.max(monthData.length - 1, 1);

  ctx.strokeStyle = "rgba(255, 255, 255, 0.15)";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(padding, padding);
  ctx.lineTo(padding, padding + plotHeight);
  ctx.lineTo(padding + plotWidth, padding + plotHeight);
  ctx.stroke();

  const horizontalLines = Math.max(2, Math.min(6, Math.floor(maxProfit / profitStep)));
  ctx.setLineDash([4, 6]);
  for (let i = 1; i <= horizontalLines; i++) {
    const value = maxProfit - i * profitStep;
    const y = padding + (1 - value / maxProfit) * plotHeight;
    ctx.beginPath();
    ctx.moveTo(padding, y);
    ctx.lineTo(padding + plotWidth, y);
    ctx.stroke();

    ctx.fillStyle = "#f5f8fa";
    ctx.font = "700 16px 'Space Grotesk', sans-serif";
    ctx.fillText(`$${value.toLocaleString()}`, padding + 6, y - 6);
  }
  ctx.setLineDash([]);

  order.forEach((plan, planIndex) => {
    const color = planColors[plan] || "#9ba7b4";
    ctx.strokeStyle = color;
    ctx.lineWidth = 4;
    ctx.beginPath();

    monthData.forEach((month, monthIndex) => {
      const profit = month.plans?.[plan]?.profit || 0;
      const x = padding + monthIndex * xStep;
      const y = padding + plotHeight - (profit / maxProfit) * plotHeight;
      if (monthIndex === 0) {
        ctx.moveTo(x, y);
      } else {
        ctx.lineTo(x, y);
      }

      ctx.fillStyle = color;
      ctx.beginPath();
       ctx.arc(x, y, 7, 0, Math.PI * 2);
      ctx.fill();
    });

    ctx.stroke();

    const lastMonth = monthData[monthData.length - 1];
    const lastProfit = lastMonth.plans?.[plan]?.profit || 0;
    const labelX = padding + (monthData.length - 1) * xStep + 8;
    const labelY = padding + plotHeight - (lastProfit / maxProfit) * plotHeight;
    ctx.fillStyle = color;
    ctx.font = "800 18px 'Space Grotesk', sans-serif";
    ctx.fillText(`$${Math.round(lastProfit).toLocaleString()}`, labelX, labelY - 6);
  });

  ctx.fillStyle = "#f5f8fa";
  ctx.font = "700 15px 'Space Grotesk', sans-serif";
  monthData.forEach((month, monthIndex) => {
    const x = padding + monthIndex * xStep;
    ctx.save();
    ctx.translate(x, padding + plotHeight + 16);
    ctx.rotate(-Math.PI / 6);
    ctx.textAlign = "right";
    ctx.fillText(month.month.slice(0, 3), 0, 0);
    ctx.restore();
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
  renderHoursChart();
  renderMonthlyProfitChart();
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
    const previousSelection = selectedPlanKey;
    setSubscribeStatus(
      `Welcome, ${data.user.full_name}! You're now part of ${data.plan}.`,
      "success"
    );
    userSummary = data.summary;
    if (apiAvailable) {
      try {
        monthlyPerformance = applyCostModel(await fetchJSON("/api/analytics/monthly"));
      } catch (error) {
        console.warn("Unable to refresh monthly projection after subscribe:", error);
      }
    }
    syncFavoriteFromPurchases();
    renderAnalytics();
    renderPlanGrid();
    renderComparisonTable();
    populateSelect();
    const targetPlan = previousSelection || favoritePlanKey || planOrder[0];
    if (targetPlan) {
      selectPlan(targetPlan);
    }
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
          <strong>${user.full_name}</strong> - ${user.favorite_genre}<br />
          ${user.preferred_device} - ${user.hours_per_month} hrs/mo
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
  if (!plan) return;
  selectedPlanKey = planKey;
  planSelect.value = planKey;
  selectedPlanName.innerHTML = `${plan.name} membership ${
    plan.is_favorite
      ? '<span class="favorite-chip favorite-chip--inline">Most popular</span>'
      : ""
  }`;
  selectedPlanTagline.textContent = `${plan.tagline} - ${plan.description} ${plan.best_for}`;
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
    const [planPayload, summaryPayload, monthlyPayload] = await Promise.all([
      fetchJSON("/api/plans"),
      fetchJSON("/api/users/summary"),
      fetchJSON("/api/analytics/monthly"),
    ]);
    setPlanData(planPayload);
    userSummary = summaryPayload;
    monthlyPerformance = applyCostModel(monthlyPayload);
    apiAvailable = true;
  } catch (error) {
    console.warn("Falling back to static data:", error);
    setPlanData(fallbackPlanPayload);
    userSummary = fallbackSummary;
    monthlyPerformance = applyCostModel(fallbackMonthlyPerformance);
    apiAvailable = false;
  }

  syncFavoriteFromPurchases();
  renderPlanGrid();
  populateSelect();
  renderComparisonTable();
  renderAnalytics();
  attachEvents();
  const initialPlan = favoritePlanKey || planOrder[0];
  if (initialPlan) {
    selectPlan(initialPlan);
  }
  updateSubscribeUI();
}

document.addEventListener("DOMContentLoaded", init);
