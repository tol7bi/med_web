function showModal() {
    var overlay = document.querySelector('.overlay');
    overlay.style.display = 'flex';
}

// Функция для скрытия всплывающего окна
function closeModal() {
    var overlay = document.querySelector('.overlay');
    overlay.style.display = 'none';
}

function showIsPregnancy() {
    var gender = document.querySelector('input[name="gender"]:checked');
    var age = document.querySelector('input[name="age"]');
    var checkboxItem = document.querySelector('input[type=checkbox]');
    var checkboxdiv = document.querySelector('.checkbox-item')
    // var isPregnancy = document.querySelector('input[name="ispregnancy"]');
    // var pregnancyWeeks = document.querySelector('.pregnancy');
    var pregnancydiv = document.querySelector(".pregnancy-weeks");
    var pregnancyInput = document.querySelector('input[name="pregnancy"]')

    if (gender && gender.value === "F" && age && age.value >= 15 && age.value <= 60) {
        checkboxdiv.style.display = "block";
    } else {
        checkboxdiv.style.display = "none";
    }


    if (checkboxItem.checked && gender && gender.value === "F" && age && age.value >= 15 && age.value <= 60) {
        // console.log(pregnancyInput);
        // console.log(checkboxItem);

        pregnancydiv.style.display = "block";
        pregnancydiv.setAttribute('required', 'required')
    } else {
        console.log(checkboxItem.checked);

        checkboxItem.checked = false;

        pregnancydiv.style.display = "none";
        pregnancydiv.removeAttribute('required');
        pregnancyInput.value = '';
    }
}


function showPregnancyWeeks() {
    var gender = document.querySelector('input[name="gender"]:checked');
    var isPregnancy = document.querySelector('input[name="ispregnancy"]:checked');
    var pregnancyWeeks = document.querySelector('.pregnancy-weeks');


    if (isPregnancy && gender && gender.value === "female") {
        pregnancyWeeks.style.display = "block";
    } else {
        pregnancyWeeks.style.display = "none";
    }
}

function startNewDiagnosis() {
    localStorage.clear();
    const xhr = new XMLHttpRequest();
    xhr.open('GET', "/new_diagnostics/", true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // Действия после успешного выполнения запроса
            window.location.href = "/"; // Перенаправление пользователя
        }
    };
    xhr.send();
}

function submitForm(url) {
    var form = document.getElementById('form');
    // alert('hhh');  
    // Создайте объект для AJAX-запроса
    var xhr = new XMLHttpRequest();
    xhr.open('POST', form.action, true);

    // Отправьте форму с использованием AJAX
    xhr.send(new FormData(form));
    // Установите обработчик события для завершения запроса
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            // Обработка успешного ответа от сервера
            // Перенаправьте пользователя на указанную страницу
            if (response.error) {
                // Вывести сообщение об ошибке пользователю
                alert(response.error);
            }
            if (response.redirect) {
                // Перенаправление пользователя на указанную страницу
                window.location.href = url;
            }
        }
    };
    saveFormData();
}

// Функция для отображения модального окна
function showContactModal() {
    var modalOverlay = document.querySelector('.overlay-contact');
    modalOverlay.style.display = 'flex';
}

function showForm() {
    var modalOverlay = document.querySelector('.overlay-form');
    modalOverlay.style.display = 'flex';
}

function closeForm() {
    var modalOverlay = document.querySelector('.overlay-form');
    modalOverlay.style.display = 'none';
}

function showFormServices() {
    var modalOverlay = document.querySelector('.overlay-form-services');
    modalOverlay.style.display = 'flex';
}

function closeFormServices() {
    var modalOverlay = document.querySelector('.overlay-form-services');
    modalOverlay.style.display = 'none';
}

function closeDelete(serviceId) {
    // Открываем модальное окно
    var modal = document.getElementById('deleteConfirmationModal');
    modal.style.display = 'none';

    // Передаем id услуги для удаления в функцию удаления
    document.getElementById('deleteServiceId').value = serviceId;
}

function showRules() {
    var modalOverlay = document.querySelector('.overlay-documents-rules');
    modalOverlay.style.display = 'flex';
}

function closeRules() {
    var modalOverlay = document.querySelector('.overlay-documents-rules');
    modalOverlay.style.display = 'none';
}

function showPrivacy() {
    var modalOverlay = document.querySelector('.overlay-documents-privacy');
    modalOverlay.style.display = 'flex';
}

function closePrivacy() {
    var modalOverlay = document.querySelector('.overlay-documents-privacy');
    modalOverlay.style.display = 'none';
}

function showConsult() {
    var modalOverlay = document.querySelector('.overlay-documents-consult');
    modalOverlay.style.display = 'flex';
}

function closeConsult() {
    var modalOverlay = document.querySelector('.overlay-documents-consult');
    modalOverlay.style.display = 'none';
}

function showInfo() {
    var modalOverlay = document.querySelector('.overlay-info');
    modalOverlay.style.display = 'flex';
}

function closeInfo() {
    var modalOverlay = document.querySelector('.overlay-info');
    modalOverlay.style.display = 'none';
}

// Функция для закрытия модального окна
function closeContactModal() {
    var modalOverlay = document.querySelector('.overlay-contact');
    modalOverlay.style.display = 'none';
}



function showAutocomplete() {
    const input = document.getElementById('complaintInput');
    const inputValue = input.value.toLowerCase();

    const xhr = new XMLHttpRequest();
    xhr.open('POST', "/add_complaints/", true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.send(JSON.stringify({ data: inputValue }));

    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                const matchedOptions = JSON.parse(xhr.responseText);
                const autocompleteList = document.getElementById('autocompleteList');
                if (matchedOptions.result.length > 0) {
                    autocompleteList.innerHTML = matchedOptions.result
                        .map(option => `<div class="autocomplete-item" onclick='addOptionToSelected(${JSON.stringify(option)})'>${option}</div>`)
                        .join('');
                    autocompleteList.style.display = 'block';
                } else {
                    autocompleteList.style.display = 'none';
                }
            } else {
                console.error('Ошибка запроса:', xhr.statusText);
            }
        }
    };

}

function addOptionToSelected(optionText) {
    const selectedOptions = document.getElementById('selectedOptions');

    const xhr = new XMLHttpRequest();
    xhr.open('POST', "/remove_complaint_from_set/", true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.send(JSON.stringify({ data: optionText }));

    if (optionText) {
        const option = document.createElement('div');
        option.classList.add('selected-option');
        option.innerHTML = `
      <span class="selected-option-text">${optionText}</span>
      <span class="remove-option" onclick="removeOption(this)">X</span>
      `;

        selectedOptions.appendChild(option);
        document.getElementById('complaintInput').value = ''; // Очищаем поле ввода
        hideAutocomplete(); // Скрываем выпадающий список
    }
}


function hideAutocomplete() {
    const autocompleteList = document.getElementById('autocompleteList');
    autocompleteList.innerHTML = ''; // Очищаем список вариантов
    autocompleteList.style.display = 'none';
}

function addOption(optionText) {
    const selectedOptions = document.getElementById('selectedOptions');
    const input = document.getElementById('complaintInput');

    if (optionText) {
        const option = document.createElement('div');
        option.classList.add('selected-option');
        option.innerHTML = `
      <span class="selected-option-text">${optionText}</span>
      <span class="remove-option" onclick="removeOption(this)">X</span>
      `;

        selectedOptions.appendChild(option);
        // Не обнуляйте input.value, чтобы оставить выбранный вариант в поле ввода
    }
}

function addOptionButton() {
    const input = document.getElementById('complaintInput');
    const selectedOptions = document.getElementById('selectedOptions');
    const optionText = input.value.trim();

    const xhr = new XMLHttpRequest();
    xhr.open('POST', "/add_button/", true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.send(JSON.stringify({ data: optionText }));

    if (optionText) {
        const option = document.createElement('div');
        option.classList.add('selected-option');
        option.innerHTML = `
        <span class="selected-option-text">${optionText}</span>
        <span class="remove-option" onclick="removeOption(this)">X</span>
      `;

        selectedOptions.appendChild(option);
        input.value = ''; // Очищаем поле ввода после добавления варианта
        hideAutocomplete()
    }
}

function removeOption(element) {
    const selectedOptions = document.getElementById('selectedOptions');
    const optionText = element.previousElementSibling.textContent;

    selectedOptions.removeChild(element.parentNode);

    const xhr = new XMLHttpRequest();
    xhr.open('POST', "/add_complaint_to_set/", true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.send(JSON.stringify({ data: optionText }));

}



