function openModal(modalId) {
    const modal = document.getElementById(`${modalId}-modal`);
    if (modal) {
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden'; 
    } else {
        console.error('Modal not found:', `${modalId}-modal`);
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(`${modalId}-modal`);
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto'; 
    }
}

function addLaborFunction() {
    const totalForms = document.getElementById('id_form-TOTAL_FORMS');
    const currentCount = parseInt(totalForms.value);
    
    const newForm = document.querySelector('.lf-form').cloneNode(true);
    newForm.innerHTML = newForm.innerHTML.replace(
        /form-(\d+)-/g, 
        `form-${currentCount}-`
    );
    
    document.querySelector('#labor-functions-container').appendChild(newForm);
    totalForms.value = currentCount + 1;
}

// Закрытие при клике вне окна
window.onclick = function(event) {
  if (event.target.className === 'modal') {
      event.target.style.display = 'none';
  }
}

// Обработчики для Drag & Drop
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('excel-file-input');
const fileNameDisplay = document.getElementById('file-name');

// Функция для обновления отображения имени файла
function updateFileName(file) {
    fileNameDisplay.textContent = file ? `Выбран файл: ${file.name}` : '';
}

// События Drag & Drop
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length) {
        fileInput.files = files;
        updateFileName(files[0]); 
    }
});

// Событие выбора файла через кнопку
fileInput.addEventListener('change', (e) => {
    const files = e.target.files;
    if (files.length) {
        updateFileName(files[0]);
    }
});


// Проверка существования элементов
if (!dropZone || !fileInput || !fileNameDisplay) {
    console.error('Один из элементов не найден!');
}

// Функция для обновления имени файла
function updateFileName(file) {
    if (!file) {
        fileNameDisplay.textContent = '';
        return;
    }
    console.log('Файл выбран:', file.name);
    fileNameDisplay.textContent = `Выбран файл: ${file.name}`;
}

// Обработчики событий
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    const files = e.dataTransfer.files;
    console.log('Перетащено файлов:', files.length);
    if (files.length) {
        fileInput.files = files;
        updateFileName(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    const files = e.target.files;
    console.log('Выбрано файлов:', files.length);
    if (files.length) {
        updateFileName(files[0]);
    }
});

// Логирование выбора файла через кнопку
fileInput.addEventListener('change', (e) => {
    const files = e.target.files;
    console.log('Файл выбран:', files);
    if (files.length) {
        const fileName = files[0].name;
        dropZone.innerHTML = `<p>Выбран файл: ${fileName}</p>`;
    }
});