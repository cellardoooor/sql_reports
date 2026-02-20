document.addEventListener('DOMContentLoaded', function() {
    setCurrentDateTime();
    restoreFIO();
    
    const form = document.getElementById('incidentForm');
    form.addEventListener('submit', handleSubmit);
    
    const idField = document.getElementById('incident_id');
    idField.addEventListener('blur', loadIncidentData);
});

function setCurrentDateTime() {
    const now = new Date();
    const dateStr = now.toISOString().slice(0, 10);
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    document.getElementById('event_date').value = dateStr;
    document.getElementById('event_time').value = `${hours}:${minutes}`;
}

function getEventDateTime() {
    const date = document.getElementById('event_date').value;
    const time = document.getElementById('event_time').value;
    if (date && time) {
        return `${date}T${time}`;
    }
    return '';
}

function restoreFIO() {
    const savedFIO = localStorage.getItem('incident_fio');
    if (savedFIO) {
        document.getElementById('fio').value = savedFIO;
    }
}

function saveFIO(fio) {
    localStorage.setItem('incident_fio', fio);
}

async function loadIncidentData() {
    const idField = document.getElementById('incident_id');
    const incidentId = idField.value;
    
    if (!incidentId) {
        return;
    }
    
    try {
        const response = await fetch(`/api/incident/${incidentId}`);
        
        if (response.ok) {
            const data = await response.json();
            if (data.success) {
                fillFormWithData(data.data);
                showToast('Данные загружены', 'success');
            }
        }
        // Если не найдено - ничего не делаем, молча продолжаем
    } catch (error) {
        console.error('Error loading incident:', error);
    }
}

function fillFormWithData(data) {
    document.getElementById('fio').value = data.fio || '';
    document.getElementById('tag').value = data.tag || 'Мониторинг';
    
    // Разбор даты и времени
    if (data.event_datetime) {
        const datetimeStr = data.event_datetime;
        // Формат: "2026-02-20 11:18:00" или "2026-02-20T11:18:00"
        const parts = datetimeStr.replace('T', ' ').split(' ');
        document.getElementById('event_date').value = parts[0];
        document.getElementById('event_time').value = parts[1].substring(0, 5);
    }
    
    // Обратный расчет validity_days из validity_hours
    if (data.validity_hours) {
        document.getElementById('validity_days').value = Math.floor(data.validity_hours / 24);
    } else {
        document.getElementById('validity_days').value = '';
    }
    
    document.getElementById('event_description').value = data.event_description || '';
    document.getElementById('engineer_actions').value = data.engineer_actions || '';
}

async function handleSubmit(e) {
    e.preventDefault();
    
    clearErrors();
    
    const eventDateTime = getEventDateTime();
    const validityDaysValue = document.getElementById('validity_days').value;
    const incidentId = document.getElementById('incident_id').value;
    
    const formData = {
        incident_id: incidentId ? parseInt(incidentId) : null,
        fio: document.getElementById('fio').value.trim(),
        event_datetime: eventDateTime,
        tag: document.getElementById('tag').value,
        validity_days: validityDaysValue ? parseInt(validityDaysValue) : null,
        event_description: document.getElementById('event_description').value.trim() || null,
        engineer_actions: document.getElementById('engineer_actions').value.trim() || null,
        csrf_token: document.querySelector('input[name="csrf_token"]').value
    };
    
    if (!validateForm(formData)) {
        return;
    }
    
    const submitBtn = document.querySelector('.submit-btn');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Отправка...';
    
    try {
        const response = await fetch('/api/incident', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            const messageWithId = `${result.message} (ID: ${result.id})`;
            showToast(messageWithId, 'success');
            saveFIO(formData.fio);
            resetForm();
        } else {
            if (result.errors) {
                Object.keys(result.errors).forEach(field => {
                    showFieldError(field, result.errors[field]);
                });
            }
            showToast(result.message || 'Ошибка при регистрации', 'error');
        }
    } catch (error) {
        showToast('Ошибка соединения с сервером', 'error');
        console.error('Error:', error);
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Зарегистрировать событие';
    }
}

function validateForm(data) {
    let isValid = true;
    
    if (!data.fio || data.fio.length < 2) {
        showFieldError('fio', 'ФИО должно содержать минимум 2 символа');
        isValid = false;
    }
    
    if (!data.event_datetime) {
        showFieldError('event_datetime', 'Дата и время обязательны');
        isValid = false;
    }
    
    if (!data.tag) {
        showFieldError('tag', 'Выберите тег');
        isValid = false;
    }
    
    // Проверка актуальности только если заполнено
    if (data.validity_days !== null && (data.validity_days < 1 || data.validity_days > 365)) {
        showFieldError('validity_days', 'Значение должно быть от 1 до 365');
        isValid = false;
    }
    
    // Проверка формата времени (должен быть HH:MM, 24-часовой)
    if (data.event_datetime) {
        const timeMatch = data.event_datetime.match(/T(\d{2}):(\d{2})$/);
        if (!timeMatch) {
            showFieldError('event_datetime', 'Неверный формат времени (ЧЧ:ММ, например: 14:30)');
            isValid = false;
        } else {
            const hours = parseInt(timeMatch[1]);
            const minutes = parseInt(timeMatch[2]);
            if (hours > 23 || minutes > 59) {
                showFieldError('event_datetime', 'Неверное время (часы: 00-23, минуты: 00-59)');
                isValid = false;
            }
        }
    }
    
    return isValid;
}

function showFieldError(fieldName, message) {
    const errorElement = document.getElementById(`${fieldName}-error`);
    if (errorElement) {
        errorElement.textContent = message;
    }
    
    const inputElement = document.getElementById(fieldName);
    if (inputElement) {
        inputElement.style.borderColor = '#e74c3c';
    }
    
    // Special handling for datetime errors
    if (fieldName === 'event_datetime') {
        const dateElement = document.getElementById('event_date');
        const timeElement = document.getElementById('event_time');
        if (dateElement) dateElement.style.borderColor = '#e74c3c';
        if (timeElement) timeElement.style.borderColor = '#e74c3c';
    }
}

function clearErrors() {
    document.querySelectorAll('.error').forEach(el => {
        el.textContent = '';
    });
    
    document.querySelectorAll('input, select, textarea').forEach(el => {
        el.style.borderColor = '#e0e0e0';
    });
}

function resetForm() {
    document.getElementById('incident_id').value = '';
    setCurrentDateTime();
    document.getElementById('fio').value = '';
    document.getElementById('tag').value = 'Мониторинг';
    document.getElementById('validity_days').value = '';
    document.getElementById('event_description').value = '';
    document.getElementById('engineer_actions').value = '';
}

function showToast(message, type) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 4000);
}
