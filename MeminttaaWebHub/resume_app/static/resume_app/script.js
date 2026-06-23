const portfolioData = {
    skills: [
        {
            category: "Языки программирования",
            items: ["Python (Скрипты, Django, Flask)", "Go (Разработка микросервисов)", "Java (Консольные приложения, Spring)", "C# (WinForms, WPF)", "HTML5 / CSS3 / JavaScript"]
        },
        {
            category: "Веб-инженерия & Компьютерное зрение",
            items: ["Django Framework", "FastAPI (ASGI асинхронные микросервисы)", "OpenCV (МДК 01.01 Библиотеки Face Recognition)", "Node.js", "React.js"]
        },
        {
            category: "Базы данных (СУБД) & Моделирование",
            items: ["PostgreSQL (Основное хранилище проекта)", "MySQL / Workbench (Проектирование EER моделей)", "SQLite", "SQLAlchemy ORM"]
        },
        {
            category: "DevOps & Системная среда",
            items: ["Docker / Контейнеризация сервисов", "Git / GitHub / GitLab (Контроль версий)", "Linux Bash / Администрирование", "CI/CD автоматизация"]
        }
    ],
    coursesAndProjects: [
        {
            type: "mdk",
            tag: "Курсовой проект (2025)",
            title: "Проектирование ЛВС центрального подразделения спорткомплекса",
            tech: "MySQL, Draw.io, СУБД, Релейная защита",
            desc: "Разработка технического предложения отказоустойчивой локальной сети спортивного комплекса. Построение EER-диаграмм баз данных управления устройствами (таблицы Devices, Price, Place, Users), разграничение прав доступа и топологическое планирование СКС."
        },
        {
            type: "course",
            tag: "Групповой проект",
            title: "Шоколадная фабрика «Dinker»: Desktop ERP",
            tech: "PyQt6, Python, SQLite / СУБД",
            desc: "Разработка корпоративного настольного приложения для автоматизации шоколадного производства. Реализованы модули: интерактивная графическая карта опасных зон фабрики, калькулятор рецептуры сортов шоколада с динамическим пересчетом ингредиентов, система аналитики и контроля партий."
        },
        {
            type: "course",
            tag: "Разработка",
            title: "Telegram Bot: Документооборот & Базы Данных",
            tech: "Python, Telebot / Aiogram, SQLite",
            desc: "Интеллектуальный чат-бот для автоматизации студенческих и административных задач. Интегрирован с базой данных SQLite для ведения логов, учета ролей и безопасного распределенного доступа к файлам."
        },
        {
            type: "course",
            tag: "Автоматизация",
            title: "Python-генератор документов по шаблонам",
            tech: "Python, DocxTemplate, OpenPyXL",
            desc: "Скрипт автоматического рендеринга официальной документации. Извлекает структурированные списки студентов и оценки из Excel-таблиц и налету генерирует персонализированные справки, ведомости и отчеты в формате .docx."
        }
    ],
    sdlc: [
        { step: "1. Requirements", desc: "Изучение ТЗ, систематизация сетевых требований администрации, сбор метрик здания.", tools: "Notion, Miro" },
        { step: "2. Design", desc: "Построение логических и реляционных моделей баз данных, проектирование EER и UI.", tools: "Draw.io, MySQL Workbench, Figma" },
        { step: "3. Development", desc: "Написание бэкенда на Python/Django/FastAPI, асинхронных хэндлеров и десктопной логики.", tools: "VS Code, Git" },
        { step: "4. Testing", desc: "Автоматизация тестирования API, отладка SQL запросов, проверка граничных условий калькуляторов.", tools: "Pytest, Postman" },
        { step: "5. Deploy & Ops", desc: "Контейнеризация веб-приложений, Docker-деплой, администрирование в PostgreSQL.", tools: "Docker, Bash" }
    ]
};

document.addEventListener('DOMContentLoaded', () => {
    const skillsGrid = document.getElementById('skillsGrid');
    if (skillsGrid) {
        portfolioData.skills.forEach(skillCat => {
            const card = document.createElement('div');
            card.className = 'card skill-category-card game-card-effect';
            let itemsHtml = skillCat.items.map(item => `<li>${item}</li>`).join('');
            card.innerHTML = `<h3>${skillCat.category}</h3><ul>${itemsHtml}</ul>`;
            skillsGrid.appendChild(card);
        });
    }

    const projectsGrid = document.getElementById('projectsGrid');
    if (projectsGrid) {
        portfolioData.coursesAndProjects.forEach(item => {
            const card = document.createElement('div');
            card.className = `card dynamic-card game-card-effect ${item.type}-type`;
            card.innerHTML = `
                <span class="tag mdk-badge">${item.tag}</span>
                <h3>${item.title}</h3>
                <p class="card-desc">${item.desc}</p>
                <p class="card-tech"><strong>Стек:</strong> ${item.tech}</p>
            `;
            projectsGrid.appendChild(card);
        });
    }

    const sdlcGrid = document.getElementById('sdlcGrid');
    if (sdlcGrid) {
        portfolioData.sdlc.forEach((s, idx) => {
            const block = document.createElement('div');
            block.className = 'sdlc-item';
            block.innerHTML = `
                <div class="sdlc-num">0${idx + 1}</div>
                <strong>${s.step}</strong>
                <div class="tooltip"><p>${s.desc}</p><small>Инструменты: ${s.tools}</small></div>
            `;
            sdlcGrid.appendChild(block);
        });
    }

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => { if (entry.isIntersecting) entry.target.classList.add('active'); });
    }, { threshold: 0.05 });
    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

    const themeBtn = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');
    if (themeBtn && themeIcon) {
        themeBtn.addEventListener('click', () => {
            const body = document.body;
            const isDark = body.getAttribute('data-theme') === 'dark';
            body.setAttribute('data-theme', isDark ? 'light' : 'dark');

            if (isDark) {
                themeIcon.src = "/static/resume_app/images/sun.png";
                themeIcon.alt = "Светлая тема";
            } else {
                themeIcon.src = "/static/resume_app/images/moon.png";
                themeIcon.alt = "Темная тема";
            }
        });
    }

    initCanvasStars();
    initCertificatesModal();
});

function initCanvasStars() {
    const canvas = document.getElementById('heroCanvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let stars = [];
    const starTypes = ['✦', '★', '✶', '✷'];

    function resize() {
        canvas.width = canvas.parentElement.offsetWidth;
        canvas.height = canvas.parentElement.offsetHeight;
    }

    class Star {
        constructor() { this.reset(); }
        reset() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.size = Math.random() * 12 + 10;
            this.speedX = (Math.random() - 0.5) * 0.8;
            this.speedY = (Math.random() - 0.5) * 0.8;
            this.char = starTypes[Math.floor(Math.random() * starTypes.length)];
            this.angle = Math.random() * Math.PI * 2;
            this.spinSpeed = (Math.random() - 0.5) * 0.02;
            this.alpha = Math.random() * 0.3 + 0.1;
            this.glowDir = Math.random() > 0.5 ? 0.005 : -0.005;
        }
        update() {
            this.x += this.speedX;
            this.y += this.speedY;
            this.angle += this.spinSpeed;
            this.alpha += this.glowDir;
            if (this.alpha > 0.45 || this.alpha < 0.1) this.glowDir = -this.glowDir;
            if (this.x > canvas.width || this.x < 0 || this.y > canvas.height || this.y < 0) this.reset();
        }
        draw() {
            const accentColor = getComputedStyle(document.body).getPropertyValue('--accent-dark').trim();
            ctx.save();
            ctx.translate(this.x, this.y);
            ctx.rotate(this.angle);
            ctx.fillStyle = accentColor;
            ctx.globalAlpha = this.alpha;
            ctx.font = `${this.size}px serif`;
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(this.char, 0, 0);
            ctx.restore();
        }
    }

    window.addEventListener('resize', resize);
    resize();
    for (let i = 0; i < 45; i++) { stars.push(new Star()); }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        stars.forEach(s => { s.update(); s.draw(); });
        requestAnimationFrame(animate);
    }
    animate();

    const webAiAnalyzeBtn = document.getElementById('webAiAnalyzeBtn');
    const webAiText = document.getElementById('webAiText');
    const webAiVerdict = document.getElementById('webAiVerdict');

    if (webAiAnalyzeBtn) {
        webAiAnalyzeBtn.addEventListener('click', async () => {
            const text = webAiText.value.trim();
            if (!text) return alert('Пожалуйста, введите текст для анализа!');
            webAiVerdict.textContent = '🧠 ИИ думает...';
            try {
                const response = await fetch('/ai/analyze-text/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
                    body: JSON.stringify({ text: text })
                });
                const data = await response.json();
                if (data.success) {
                    webAiVerdict.textContent = `${data.verdict} (${data.confidence.toFixed(2)}%)`;
                    for (const [code, proba] of Object.entries(data.probabilities)) {
                        const bar = document.getElementById(`bar-${code}`);
                        const pct = document.getElementById(`pct-${code}`);
                        if (bar && pct) { bar.style.width = `${proba.toFixed(1)}%`; pct.textContent = `${proba.toFixed(1)}%`; }
                    }
                } else { webAiVerdict.textContent = '❌ Ошибка анализа'; }
            } catch (error) { webAiVerdict.textContent = '❌ Не удалось связаться с сервером'; }
        });
    }

    const webFaceBtn = document.getElementById('webFaceBtn');
    const webFaceInput = document.getElementById('webFaceInput');
    const webFaceVerdict = document.getElementById('webFaceVerdict');
    const faceResultsContainer = document.getElementById('webFaceResultsContainer');
    const faceNamesList = document.getElementById('webFaceNamesList');
    const faceImagePreview = document.getElementById('faceImagePreview');

    if (webFaceInput) {
        webFaceInput.addEventListener('change', function () {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    faceImagePreview.src = e.target.result;
                    faceImagePreview.style.display = 'block';
                }
                reader.readAsDataURL(file);
            } else {
                faceImagePreview.src = '';
                faceImagePreview.style.display = 'none';
            }
        });
    }

    if (webFaceBtn) {
        webFaceBtn.addEventListener('click', async () => {
            if (!webFaceInput.files || webFaceInput.files.length === 0) return alert('Пожалуйста, выберите фото группы!');
            webFaceVerdict.textContent = '👁⚡ Идет асинхронное сканирование dlib...';
            faceResultsContainer.style.display = 'none';
            const formData = new FormData();
            formData.append('file', webFaceInput.files[0]);
            try {
                const response = await fetch('/ai/recognize-faces/', {
                    method: 'POST',
                    headers: { 'X-CSRFToken': getCookie('csrftoken') },
                    body: formData
                });
                const data = await response.json();
                if (data.success) {
                    webFaceVerdict.textContent = `🎯 Анализ завершен! Найдено лиц: ${data.faces_count}`;
                    if (data.names.length > 0) {
                        faceResultsContainer.style.display = 'block';
                        faceNamesList.textContent = data.names.join(', ');
                    } else {
                        faceResultsContainer.style.display = 'block';
                        faceNamesList.textContent = 'Студенты группы не обнаружены (Unknown)';
                    }
                } else { webFaceVerdict.textContent = '❌ Ошибка при обработке изображения'; }
            } catch (error) {
                webFaceVerdict.textContent = '❌ Ошибка сети или сервера';
            }
        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
}

function initCertificatesModal() {
    const modal = document.getElementById("certModal");
    const modalImg = document.getElementById("modalTargetImg");
    const captionText = document.getElementById("modalCaption");
    const closeBtn = document.getElementsByClassName("modal-close")[0];

    document.querySelectorAll('.cert-img-container').forEach(container => {
        container.addEventListener('click', function () {
            const img = this.querySelector('.cert-thumbnail');
            const card = this.closest('.cert-card');
            const title = card.querySelector('h3').textContent;
            modal.style.display = "block";
            modalImg.src = img.src;
            captionText.textContent = title;
        });
    });

    if (closeBtn) closeBtn.addEventListener('click', () => { modal.style.display = "none"; });
    if (modal) modal.addEventListener('click', (e) => { if (e.target === modal) modal.style.display = "none"; });
}