document.addEventListener('DOMContentLoaded', function() {
    const calendar = document.getElementById('calendar');
    const eventForm = document.getElementById('eventForm');
    const eventDateInput = document.getElementById('eventDate');
    const eventFormContainer = document.getElementById('event-form');
    const backToMonthsBtn = document.getElementById('back-to-months');
    const monthSelection = document.getElementById('month-selection');
    const monthButtons = document.querySelectorAll('.month-btn');
    const eventList = document.getElementById('event-list');
    const eventsUl = document.getElementById('events');

    const currentYear = new Date().getFullYear();
    let events = [];

    function generateCalendar(year, month) {
        calendar.innerHTML = '';
        const daysInMonth = new Date(year, month + 1, 0).getDate();

        for (let i = 1; i <= daysInMonth; i++) {
            const dayDiv = document.createElement('div');
            dayDiv.className = 'day';
            dayDiv.textContent = i;
            dayDiv.addEventListener('click', function() {
                selectDate(year, month, i);
            });
            calendar.appendChild(dayDiv);
        }

        calendar.style.display = 'grid';
        backToMonthsBtn.style.display = 'inline-block';
        monthSelection.style.display = 'none';
    }

    function selectDate(year, month, day) {
        const days = document.querySelectorAll('.day');
        days.forEach(day => day.classList.remove('selected'));
        eventDateInput.value = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
        eventFormContainer.style.display = 'block';
        eventDateInput.closest('.day').classList.add('selected');
    }

    eventForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const newEvent = {
            eventDate: eventDateInput.value,
            eventTitle: document.getElementById('eventTitle').value,
            eventDescription: document.getElementById('eventDescription').value,
        };

        // Adicionar evento à lista de eventos
        events.push(newEvent);
        displayEvents();

        // Resetar o formulário
        eventForm.reset();
        eventFormContainer.style.display = 'none';
    });

    function displayEvents() {
        eventsUl.innerHTML = '';
        eventList.style.display = 'block';

        events.forEach((event, index) => {
            const li = document.createElement('li');
            li.className = 'event-item';
            li.innerHTML = `
                <span><strong>${event.eventDate}</strong> - ${event.eventTitle}: ${event.eventDescription}</span>
                <button class="remove-event-btn" data-index="${index}">Remover</button>
            `;
            eventsUl.appendChild(li);
        });

        // Adicionar funcionalidade de remoção
        const removeButtons = document.querySelectorAll('.remove-event-btn');
        removeButtons.forEach(button => {
            button.addEventListener('click', function() {
                const index = this.getAttribute('data-index');
                removeEvent(index);
            });
        });
    }

    function removeEvent(index) {
        events.splice(index, 1);
        displayEvents();
    }

    monthButtons.forEach(button => {
        button.addEventListener('click', function() {
            const month = parseInt(this.getAttribute('data-month'));
            generateCalendar(currentYear, month);
        });
    });

    backToMonthsBtn.addEventListener('click', function() {
        calendar.style.display = 'none';
        eventFormContainer.style.display = 'none';
        eventList.style.display = 'none';
        backToMonthsBtn.style.display = 'none';
        monthSelection.style.display = 'grid';
    });
});
