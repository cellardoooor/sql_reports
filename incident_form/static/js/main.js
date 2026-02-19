document.addEventListener('DOMContentLoaded', function() {
    setCurrentDateTime();
    restoreFIO();
    
    const form = document.getElementById('incidentForm');
    form.addEventListener('submit', handleSubmit);
});

function setCurrentDateTime() {
    const now = new Date();
    const formatted = now.toISOString().slice(0, 16);
    document.getElementById('event_datetime').value = formatted;
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

async function handleSubmit(e) {
    e.preventDefault();
    
    clearErrors();
    
    const formData = {
        fio: document.getElementById('fio').value.trim(),
        event_datetime: document.getElementById('event_datetime').value,
        tag: document.getElementById('tag').value,
        validity_days: parseInt(document.getElementById('validity_days').value),
        event_description: document.getElementById('event_description').value.trim(),
        engineer_actions: document.getElementById('engineer_actions').value.trim(),
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
            showToast(result.message, 'success');
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
        submitBtn.textContent = 'Зарегистрировать инцидент';
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
    
    if (!data.validity_days || data.validity_days < 1 || data.validity_days > 365) {
        showFieldError('validity_days', 'Значение должно быть от 1 до 365');
        isValid = false;
    }
    
    if (!data.event_description || data.event_description.length < 10) {
        showFieldError('event_description', 'Описание должно содержать минимум 10 символов');
        isValid = false;
    }
    
    if (!data.engineer_actions) {
        showFieldError('engineer_actions', 'Укажите действия инженера');
        isValid = false;
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
    document.getElementById('event_datetime').value = new Date().toISOString().slice(0, 16);
    document.getElementById('tag').value = '';
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
