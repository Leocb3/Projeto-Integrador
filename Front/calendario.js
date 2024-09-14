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
    let editEventId = null; // Variável para armazenar o ID do evento que está sendo editado

    // Função para carregar eventos do backend (GET)
    async function fetchEventos() {
        try {
            const response = await fetch('http://127.0.0.1:5000/eventos');
            const eventosData = await response.json();
            events = eventosData;
            displayEvents();
        } catch (error) {
            console.error('Erro ao buscar eventos:', error);
        }
    }

    // Função para adicionar evento ao backend (POST)
    async function addEvento(evento) {
        try {
            const response = await fetch('http://127.0.0.1:5000/eventos', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(evento),
            });
            if (response.ok) {
                fetchEventos(); // Atualiza os eventos após adicionar
            }
        } catch (error) {
            console.error('Erro ao adicionar evento:', error);
        }
    }

    // Função para atualizar evento no backend (PUT)
    async function updateEvento(evento) {
        try {
            const response = await fetch(`http://127.0.0.1:5000/eventos/${evento.id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(evento),
            });
            if (response.ok) {
                fetchEventos(); // Atualiza os eventos após a edição
            }
        } catch (error) {
            console.error('Erro ao atualizar evento:', error);
        }
    }

    // Função para remover evento do backend (DELETE)
    async function deleteEvento(eventId) {
        try {
            const response = await fetch(`http://127.0.0.1:5000/eventos/${eventId}`, {
                method: 'DELETE',
            });
            if (response.ok) {
                fetchEventos(); // Atualiza os eventos após remoção
            }
        } catch (error) {
            console.error('Erro ao remover evento:', error);
        }
    }

    // Carregar eventos ao inicializar
    fetchEventos();

    // Gerar calendário
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

    // Selecionar uma data e mostrar o formulário de eventos
    function selectDate(year, month, day) {
        const days = document.querySelectorAll('.day');
        days.forEach(day => day.classList.remove('selected'));
        eventDateInput.value = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
        eventFormContainer.style.display = 'block';
        eventDateInput.closest('.day').classList.add('selected');
    }

    // Submeter novo evento ou editar evento existente
    eventForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const newEvent = {
            usuario_id: 1, // Valor fixo como exemplo, você pode modificar conforme necessário
            titulo: document.getElementById('eventTitle').value,
            descricao: document.getElementById('eventDescription').value,
            data_evento: eventDateInput.value
        };

        if (editEventId) {
            newEvent.id = editEventId; // Adiciona o ID do evento que está sendo editado
            updateEvento(newEvent); // Atualiza o evento no backend
            editEventId = null; // Reseta a variável de edição após salvar
        } else {
            addEvento(newEvent); // Adiciona o evento no backend
        }

        // Resetar o formulário
        eventForm.reset();
        eventFormContainer.style.display = 'none';
    });

    // Exibir eventos no front-end
    function displayEvents() {
        eventsUl.innerHTML = '';
        eventList.style.display = 'block';

        events.forEach((event, index) => {
            const li = document.createElement('li');
            li.className = 'event-item';
            li.innerHTML = `
                <span><strong>${event.data_evento}</strong> - ${event.titulo}: ${event.descricao}</span>
                <button class="edit-event-btn" data-id="${event.id}">Editar</button>
                <button class="remove-event-btn" data-id="${event.id}">Remover</button>
            `;
            eventsUl.appendChild(li);
        });

        // Adicionar funcionalidade de remoção
        const removeButtons = document.querySelectorAll('.remove-event-btn');
        removeButtons.forEach(button => {
            button.addEventListener('click', function() {
                const eventId = this.getAttribute('data-id');
                deleteEvento(eventId); // Remove evento do backend
            });
        });

        // Adicionar funcionalidade de edição
        const editButtons = document.querySelectorAll('.edit-event-btn');
        editButtons.forEach(button => {
            button.addEventListener('click', function() {
                const eventId = this.getAttribute('data-id');
                const eventToEdit = events.find(event => event.id == eventId);
                if (eventToEdit) {
                    // Preenche o formulário com os dados do evento a ser editado
                    document.getElementById('eventTitle').value = eventToEdit.titulo;
                    document.getElementById('eventDescription').value = eventToEdit.descricao;
                    eventDateInput.value = eventToEdit.data_evento;
                    eventFormContainer.style.display = 'block';
                    editEventId = eventToEdit.id; // Armazena o ID do evento que está sendo editado
                }
            });
        });
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
