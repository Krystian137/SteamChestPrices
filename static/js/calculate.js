let fieldCounter = 1;

document.getElementById('add_button').addEventListener('click', function () {
    const container = document.getElementById('fields-container');

    const newFields = document.createElement('div');
    newFields.classList.add('row', 'mb-3'); // Stałe odstępy między polami

    // Select dla skrzyń
    const selectDiv = document.createElement('div');
    selectDiv.classList.add('col-md-4');
    const select = document.createElement('select');
    select.name = 'case_code[]';
    select.classList.add('form-select');
    select.required = true;

    // Opcje dla select
    for (const chestName in casesData) {
        const option = document.createElement('option');
        option.value = casesData[chestName].code;
        option.textContent = `${chestName} - ${casesData[chestName].latest_price}`;
        select.appendChild(option);
    }
    selectDiv.appendChild(select);

    // Input dla ilości
    const inputDiv = document.createElement('div');
    inputDiv.classList.add('col-md-2');
    const input = document.createElement('input');
    input.type = 'number';
    input.name = 'quantity[]';
    input.classList.add('form-control');
    input.min = 1;
    input.required = true;
    inputDiv.appendChild(input);

    // Przycisk "Usuń"
    const removeButtonDiv = document.createElement('div');
    removeButtonDiv.classList.add('col-md-1', 'd-flex', 'justify-content-center', 'align-items-center');
    const removeButton = document.createElement('button');
    removeButton.type = 'button';
    removeButton.classList.add('btn', 'btn-danger');
    removeButton.textContent = 'Usuń';
    removeButton.addEventListener('click', function () {
        newFields.remove();
    });

    removeButtonDiv.appendChild(removeButton);

    // Dodanie nowych pól do kontenera
    newFields.appendChild(selectDiv);
    newFields.appendChild(inputDiv);
    newFields.appendChild(removeButtonDiv);
    container.appendChild(newFields);

    fieldCounter++;
});


