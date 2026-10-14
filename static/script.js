let allPlayersData = [];
let currentPage = 1;
const rowsPerPage = 50; 

const tableBody = document.getElementById('tableBody');
const firstBtn = document.getElementById('firstBtn');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const lastBtn = document.getElementById('lastBtn');
const pageInput = document.getElementById('pageInput');
const totalPagesSpan = document.getElementById('totalPages');

function renderTablePage(page) {
    const totalPages = Math.ceil(allPlayersData.length / rowsPerPage);
    
    if (page < 1) page = 1;
    if (page > totalPages) page = totalPages;
    currentPage = page;

    tableBody.innerHTML = "";
    
    const startIndex = (currentPage - 1) * rowsPerPage;
    const endIndex = startIndex + rowsPerPage;
    const pageData = allPlayersData.slice(startIndex, endIndex);

    pageData.forEach((p, index) => {
        const tr = document.createElement('tr');
        const absoluteRank = startIndex + index + 1;
        
        tr.innerHTML = `
            <td>${absoluteRank}</td>
            <td>
                <div class="player-info">
                    <span title="${p.country}" style="cursor: help; font-size: 1.2em;">${p.flag}</span>
                    <span class="player-name">${p.name}</span>
                </div>
            </td>
            <td class="global-rank">#${p.global_position.toLocaleString()}</td>
            <td class="player-score">${p.points.toLocaleString()}</td>
        `;
        tableBody.appendChild(tr);
    });

    pageInput.value = currentPage;
    totalPagesSpan.textContent = totalPages;
    
    firstBtn.disabled = currentPage === 1;
    prevBtn.disabled = currentPage === 1;
    nextBtn.disabled = currentPage === totalPages || totalPages === 0;
    lastBtn.disabled = currentPage === totalPages || totalPages === 0;
    
    pageInput.disabled = totalPages === 0;
    pageInput.max = totalPages;
}

firstBtn.addEventListener('click', () => renderTablePage(1));
prevBtn.addEventListener('click', () => renderTablePage(currentPage - 1));
nextBtn.addEventListener('click', () => renderTablePage(currentPage + 1));
lastBtn.addEventListener('click', () => {
    const totalPages = Math.ceil(allPlayersData.length / rowsPerPage);
    renderTablePage(totalPages);
});

pageInput.addEventListener('change', (e) => {
    let requestedPage = parseInt(e.target.value, 10);
    if (isNaN(requestedPage)) requestedPage = currentPage; 
    renderTablePage(requestedPage);
});

document.getElementById('startBtn').addEventListener('click', async () => {
    const uid = document.getElementById('uid').value.trim();
    const region = document.getElementById('region').value.trim();
    const pages = document.getElementById('pages').value.trim();
    
    const startBtn = document.getElementById('startBtn');
    const loader = document.getElementById('loader');
    const statusMessage = document.getElementById('statusMessage');
    const tableContainer = document.getElementById('tableContainer');

    if (!uid || !region || !pages) {
        alert("Please fill in all fields.");
        return;
    }

    startBtn.disabled = true;
    loader.style.display = "block";
    tableContainer.style.display = "none";
    
    statusMessage.style.display = "block";
    statusMessage.textContent = `Searching players in ${region}... This might take a moment.`;

    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ uid, region, pages })
        });

        if (!response.ok) throw new Error("Server or Network error");

        allPlayersData = await response.json(); 
        statusMessage.style.display = "none"; 

        if (allPlayersData.length === 0) {
            statusMessage.style.display = "block";
            statusMessage.textContent = "No players found in this leaderboard range.";
        } else {
            tableContainer.style.display = "block";
            renderTablePage(1);
        }
    } catch (error) {
        statusMessage.style.display = "block";
        statusMessage.textContent = `[ERROR] ${error.message}`;
    } finally {
        startBtn.disabled = false;
        loader.style.display = "none";
    }
});