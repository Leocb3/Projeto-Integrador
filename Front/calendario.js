document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const usuarioId = urlParams.get('usuario_id');
    const calendarContainer = document.getElementById('calendar-container');
    const calendarElement = document.getElementById('calendar');
    const eventForm = document.getElementById('event-form');
    const eventList = document.getElementById('event-list');
    const backToMonthsButton = document.getElementById('back-to-months');
    const monthButtons = document.querySelectorAll('.month-btn');
    const eventFormEl = document.getElementById('eventForm');
    const eventDateEl = document.getElementById('eventDate');
    const eventsUl = document.getElementById('events');

    let currentMonth = new Date().getMonth();
    let selectedDate = null;

    function loadCalendar(month) {
        const now = new Date();
        now.setMonth(month);
        now.setDate(1);

        const monthName = now.toLocaleString('pt-BR', { month: 'long' });
        calendarElement.innerHTML = `<h2>${monthName} ${now.getFullYear()}</h2>`;

        const daysInMonth = new Date(now.getFullYear(), now.getMonth() + 1, 0).getDate();

        const daysContainer = document.createElement('div');
        daysContainer.classList.add('days-container');

        for (let i = 1; i <= daysInMonth; i++) {
            const day = document.createElement('div');
            day.classList.add('day');
            day.textContent = i;
            day.dataset.date = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
            day.addEventListener('click', showEventForm);
            daysContainer.appendChild(day);
        }

        calendarElement.appendChild(daysContainer);
        calendarElement.style.display = 'block';
        backToMonthsButton.style.display = 'inline-block';
    }

    function showEventForm(event) {
        selectedDate = event.target.dataset.date;
        eventDateEl.value = selectedDate;
        eventForm.style.display = 'block';
        loadEvents(selectedDate);
    }

    function hideEventForm() {
        eventForm.style.display = 'none';
    }

    function saveEvent(event) {
        event.preventDefault();
        
        const title = eventFormEl.eventTitle.value;
        const description = eventFormEl.eventDescription.value;

        fetch(`http://127.0.0.1:5000/eventos/criar`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                usuario_id: usuarioId,
                data: selectedDate,
                titulo: title,
                descricao: description
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
                loadEvents(selectedDate);
                hideEventForm();
            } else {
                alert('Erro ao salvar o evento.');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao se comunicar com o servidor.');
        });
    }

    function loadEvents(date) {
        fetch(`http://127.0.0.1:5000/eventos/${usuarioId}?data=${date}`)
        .then(response => response.json())
        .then(data => {
            eventsUl.innerHTML = '';
            data.eventos.forEach(evento => {
                const li = document.createElement('li');
                li.textContent = `${evento.titulo}: ${evento.descricao}`;
                eventsUl.appendChild(li);
            });
            eventList.style.display = 'block';
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao carregar eventos.');
        });
    }

    function showMonthView() {
        calendarElement.style.display = 'none';
        backToMonthsButton.style.display = 'none';
        monthButtons.forEach(button => {
            button.style.display = 'inline-block';
        });
    }

    monthButtons.forEach(button => {
        button.addEventListener('click', function() {
            const month = parseInt(button.dataset.month, 10);
            currentMonth = month;
            loadCalendar(month);
            showMonthView();
        });
    });

    backToMonthsButton.addEventListener('click', function() {
        showMonthView();
    });

    eventFormEl.addEventListener('submit', saveEvent);
});
