<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>FIDO Review Tool</title>
').filter(line => line.trim()) // simulate parsing
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
  // --- JS CODE START ---
  function handleUpload() {
    const queue = document.getElementById('projectQueue').value;
    const fileInput = document.getElementById('fileUpload');
    const file = fileInput.files[0];
    if (!file) return alert("Please select a file to upload.");

    const reader = new FileReader();
    reader.onload = function(e) {
      const content = e.target.result;
      const project = {
        name: file.name,
        type: queue,
        data: content.split('\n').filter(line => line.trim()) // simulate parsing
      };
      let stored = JSON.parse(localStorage.getItem("projects") || "[]");
      stored.push(project);
      localStorage.setItem("projects", JSON.stringify(stored));
      alert("✅ Project uploaded to " + queue + " queue.");
      fileInput.value = "";
    };
    reader.readAsText(file);
  }

  function showQueueProjects(queueType) {
    const stored = JSON.parse(localStorage.getItem("projects") || "[]");
    const filtered = stored.filter(p => p.type === queueType);
    const container = document.getElementById("mainPage");
    container.innerHTML = `<h2 class='text-xl font-semibold my-4'>${queueType.toUpperCase()} Projects</h2>`;
    if (filtered.length === 0) {
    container.innerHTML += '<p class="text-gray-600">No projects uploaded.</p>';
    return;
  }
  filtered.forEach((proj, i) => {
    const button = document.createElement("button");
    button.textContent = proj.name;
    button.className = "block w-full text-left bg-white dark:bg-gray-700 border p-3 mb-2 rounded hover:bg-blue-100 dark:hover:bg-gray-600";
    button.onclick = () => renderProjectDetail(proj);
    container.appendChild(button);
  });
}
function submitFlag() {
  const fido = document.getElementById('flagFido').value.trim();
  const submitter = document.getElementById('flagSubmitter').value.trim();
  const issue = document.getElementById('flagIssue').value.trim();
  if (!fido || !submitter || !issue) {
    alert("Please complete all fields.");
    return;
  }
  const flags = JSON.parse(localStorage.getItem("flags") || "[]");
  flags.push({ FIDO: fido, SubmittedBy: submitter, Issue: issue });
  localStorage.setItem("flags", JSON.stringify(flags));
  alert("🚩 Issue submitted and added to CATQ!");
  document.getElementById('flagFido').value = '';
  document.getElementById('flagSubmitter').value = '';
  document.getElementById('flagIssue').value = '';
  document.getElementById('flagForm').style.display = 'none';
}
function renderProjectDetail(project) {
  const container = document.getElementById("mainPage");
  container.innerHTML = `<h2 class='text-xl font-semibold my-4'>Editing: ${project.name}</h2>`;
  const table = document.createElement("table");
  table.className = "table-auto w-full border-collapse border border-gray-300 text-sm";
  const rows = project.data;
  const headers = rows[0].split(',');

  const thead = document.createElement("thead");
  const headerRow = document.createElement("tr");
  headers.forEach(h => {
    const th = document.createElement("th");
    th.textContent = h;
    th.className = "border bg-gray-100 px-2 py-1";
    headerRow.appendChild(th);
  });
  ['Updated DESCRIPTION', 'Updated CATEGORY', 'Updated BRAND', 'Action'].forEach(h => {
    const th = document.createElement("th");
    th.textContent = h;
    th.className = "border bg-gray-100 px-2 py-1";
    headerRow.appendChild(th);
  });
  thead.appendChild(headerRow);
  table.appendChild(thead);

  const tbody = document.createElement("tbody");
  for (let i = 1; i < rows.length; i++) {
    const tr = document.createElement("tr");
    const values = rows[i].split(',');
    values.forEach(v => {
      const td = document.createElement("td");
      td.textContent = v;
      td.className = "border px-2 py-1";
      tr.appendChild(td);
    });
    ['desc','cat','brand'].forEach(type => {
      const td = document.createElement("td");
      const input = document.createElement("input");
      input.className = "w-full border rounded px-1 py-0.5 text-sm";
      input.placeholder = `Edit ${type}`;
      td.appendChild(input);
      td.className = "border px-2 py-1";
      tr.appendChild(td);
    });
    const saveBtn = document.createElement("button");
    saveBtn.textContent = "💾 Save";
    saveBtn.className = "ml-2 text-sm bg-blue-500 text-white px-2 py-1 rounded hover:bg-blue-600";
    saveBtn.onclick = () => {
      const original = values;
      const updated = {
        FIDO: original[0],
        Original: {
          DESCRIPTION: original[headers.indexOf("DESCRIPTION")],
          CATEGORY: original[headers.indexOf("CATEGORY")],
          BRAND: original[headers.indexOf("BRAND")]
        },
        Updated: {
          DESCRIPTION: tr.querySelectorAll("input")[0]?.value || "",
          CATEGORY: tr.querySelectorAll("input")[1]?.value || "",
          BRAND: tr.querySelectorAll("input")[2]?.value || ""
        }
      };
      const stored = JSON.parse(localStorage.getItem(`review_${project.name}`) || "[]");
      const existingIndex = stored.findIndex(x => x.FIDO === updated.FIDO);
      if (existingIndex >= 0) stored[existingIndex] = updated;
      else stored.push(updated);
      localStorage.setItem(`review_${project.name}`, JSON.stringify(stored));
      alert(`✅ FIDO ${updated.FIDO} saved!`);
    };
    const actionTd = document.createElement("td");
    actionTd.appendChild(saveBtn);
    tr.appendChild(actionTd);
    tbody.appendChild(tr);
  
  }
  const saveAllBtn = document.createElement("button");
  saveAllBtn.textContent = "💾 Save All";
  saveAllBtn.className = "mt-4 mr-4 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700";
  saveAllBtn.onclick = () => {
    const updatedData = [];
    const rows = table.querySelectorAll("tbody tr");
    rows.forEach(row => {
      const original = [...row.querySelectorAll("td")].slice(0, headers.length).map(td => td.textContent.trim());
      const inputs = [...row.querySelectorAll("input")];
      const updated = {
        FIDO: original[0],
        Original: {
          DESCRIPTION: original[headers.indexOf("DESCRIPTION")],
          CATEGORY: original[headers.indexOf("CATEGORY")],
          BRAND: original[headers.indexOf("BRAND")]
        },
        Updated: {
          DESCRIPTION: inputs[0]?.value || "",
          CATEGORY: inputs[1]?.value || "",
          BRAND: inputs[2]?.value || ""
        }
      };
      updatedData.push(updated);
    });
    localStorage.setItem(`review_${project.name}`, JSON.stringify(updatedData));
    alert("✅ All FIDOs saved!");
  };
  container.appendChild(table);
  container.appendChild(saveAllBtn);
  
}
</script>
</head>
<body class="bg-gray-50 text-black dark:bg-gray-900 dark:text-white">
  <div class="toolbar flex justify-between items-center px-6 py-4 shadow bg-gray-800 text-white">
    <div class="text-xl font-bold">FIDO Review Tool</div>
    <div class="space-x-4">
      <button onclick="toggleFlagForm()" class="hover:underline">🚩 Flag Issue</button>
      <button onclick="showAdminPage()" class="hover:underline">🛠️ Admin</button>
      <button onclick="showMainPage()" class="hover:underline">🏠 Home</button>
      <button onclick="toggleTheme()" class="hover:underline">🌓 Toggle Theme</button>
      <button onclick="logoutUser()" class="hover:underline">🔒 Logout</button>
      <span id="welcomeUser" class="text-sm"></span>
    </div>
  </div>

  <div id="loginPanel" class="mt-24 px-4 text-black dark:text-white animate-fade-in">
    <h3 class="text-2xl font-bold mb-6 text-center">Welcome to the FIDO Review Tool</h3>
    <label class="block mb-2">Name:</label>
    <input type="text" id="loginName" class="w-full p-2 mb-4 border rounded bg-white text-black">
    <div class="mb-4">
      <label class="flex items-center mb-2 text-gray-800 dark:text-white">
        <input type="radio" name="userRole" value="reviewer" class="mr-3">
        <span>🧑 Reviewer</span>
      </label>
      <label class="flex items-center text-gray-800 dark:text-white">
        <input type="radio" name="userRole" value="admin" class="mr-3">
        <span>🛠️ Admin</span>
      </label>
    </div>
    <button onclick="loginUser()" class="w-full mt-4 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 shadow">Login</button>
  </div>

  <div id="mainPage" style="display:none">
    <div class="grid grid-cols-1 gap-6 max-w-2xl mx-auto mt-8">
      <div class="p-6 bg-blue-100 hover:bg-blue-200 border-l-4 border-blue-500 rounded shadow-md transition">
        <button class="text-blue-800 text-lg font-semibold w-full text-left" onclick="showQueueProjects('nonLicensed')">
          📂 Non-licensed FIDO Review Projects
        </button>
      </div>
      <div class="p-6 bg-green-100 hover:bg-green-200 border-l-4 border-green-500 rounded shadow-md transition">
        <button class="text-green-800 text-lg font-semibold w-full text-left" onclick="showQueueProjects('licensed')">
          📁 Licensed FIDO Review Projects
        </button>
      </div>
      <div class="p-6 bg-red-100 hover:bg-red-200 border-l-4 border-red-500 rounded shadow-md transition">
        <button class="text-red-800 text-lg font-semibold w-full text-left flex items-center" onclick="showQueueProjects('catq')">
          <span class="inline-block w-5 h-5 mr-2 bg-center bg-contain" style="background-image:url('/mnt/data/6eccc1d1-54c6-4949-9383-48902aad7019.png')"></span>
          CATQ
        </button>
      </div>
    </div>
    <!-- queue cards and admin upload will appear here -->
  </div>

  <div id="adminPage" style="display:none">
    <div class="max-w-xl mx-auto mt-8 p-6 bg-white dark:bg-gray-800 rounded shadow">
      <h2 class="text-xl font-semibold mb-4">🛠️ Upload FIDO Project</h2>
      <label for="projectQueue" class="block mb-2">Select Queue:</label>
      <select id="projectQueue" class="w-full mb-4 p-2 border rounded">
        <option value="nonLicensed">Non-licensed</option>
        <option value="licensed">Licensed</option>
        <option value="catq">CATQ</option>
      </select>
      <label for="fileUpload" class="block mb-2">Upload CSV File:</label>
      <input type="file" id="fileUpload" accept=".csv" class="w-full mb-4">
      <button onclick="handleUpload()" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Upload Project</button>
    </div>
  </div>

  <div id="flagForm" style="display:none" class="max-w-xl mx-auto mt-8 p-6 bg-white dark:bg-gray-800 rounded shadow">
    <h2 class="text-xl font-semibold mb-4">🚩 Submit a Flag</h2>
    <label class="block mb-2">Submitted by:</label>
    <input type="text" id="flagSubmitter" class="w-full p-2 mb-4 border rounded text-black" placeholder="Your name">
    <label class="block mb-2">FIDO:</label>
    <input type="text" id="flagFido" class="w-full p-2 mb-4 border rounded text-black" placeholder="FIDO ID">
    <label class="block mb-2">Issue:</label>
    <textarea id="flagIssue" class="w-full p-2 mb-4 border rounded text-black" placeholder="Describe the issue"></textarea>
    <button onclick="submitFlag()" class="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700">Submit Flag</button>
  </div>
  </div>

  <script>
    let currentUser = JSON.parse(localStorage.getItem("currentUser")) || null;

    function showMainPage() {
      document.getElementById('loginPanel').style.display = 'none';
      document.getElementById('adminPage').style.display = 'none';
      document.getElementById('mainPage').style.display = 'block';
    }

    function showAdminPage() {
      if (!currentUser || currentUser.role !== "admin") {
        alert("Access denied. Admins only.");
        return;
      }
      document.getElementById('mainPage').style.display = 'none';
      document.getElementById('adminPage').style.display = 'block';
    }

    function toggleFlagForm() {
      const form = document.getElementById('flagForm');
      form.style.display = form.style.display === 'none' ? 'block' : 'none';
    }

    function logoutUser() {
      localStorage.removeItem("currentUser");
      currentUser = null;
      document.getElementById('mainPage').style.display = 'none';
      document.getElementById('adminPage').style.display = 'none';
      document.getElementById('loginPanel').style.display = 'block';
    }

    function loginUser() {
      const username = document.getElementById('loginName').value;
      const role = document.querySelector('input[name="userRole"]:checked')?.value;
      if (username && role) {
        currentUser = { name: username, role: role };
        localStorage.setItem("currentUser", JSON.stringify(currentUser));
        document.getElementById('welcomeUser').textContent = `Welcome, ${username} (${role})`;
        document.getElementById("loginPanel").style.display = "none";
        showMainPage();
      } else {
        alert("Please enter your name and select a role.");
      }
    }

    function toggleTheme() {
      document.body.classList.toggle('dark');
    }

    if (currentUser) {
      document.getElementById("welcomeUser").textContent = `Welcome, ${currentUser.name} (${currentUser.role})`;
      showMainPage();
    } else {
      document.getElementById("loginPanel").style.display = "block";
    }
  </script>
</body>
</html>
