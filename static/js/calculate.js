document.addEventListener("DOMContentLoaded", function () {
    document.getElementById('add_button').addEventListener('click', function () {
        const container = document.getElementById('fields-container');

        const newFields = document.createElement('div');
        newFields.classList.add('row', 'mb-3', 'align-items-center', 'case-row');

        const selectDiv = document.createElement('div');
        selectDiv.classList.add('col-md-4');
        const select = document.createElement('select');
        select.name = 'case_code[]';
        select.classList.add('form-select');
        select.required = true;

        for (const chestName in casesData) {
            const option = document.createElement('option');
            option.value = casesData[chestName].code;
            option.textContent = `${chestName} - ${casesData[chestName].latest_price}`;
            select.appendChild(option);
        }
        selectDiv.appendChild(select);

        const inputDiv = document.createElement('div');
        inputDiv.classList.add('col-md-2');
        const input = document.createElement('input');
        input.type = 'number';
        input.name = 'quantity[]';
        input.classList.add('form-control');
        input.min = 1;
        input.required = true;
        inputDiv.appendChild(input);

        const removeButtonDiv = document.createElement('div');
        removeButtonDiv.classList.add('col-md-1', 'd-flex', 'justify-content-center', 'align-items-center');
        const removeButton = document.createElement('button');
        removeButton.type = 'button';
        removeButton.classList.add('btn', 'btn-danger', 'remove-btn');
        removeButton.textContent = 'Usuń';
        removeButton.addEventListener('click', function () {
            newFields.remove();
        });

        removeButtonDiv.appendChild(removeButton);

        newFields.appendChild(selectDiv);
        newFields.appendChild(inputDiv);
        newFields.appendChild(removeButtonDiv);
        container.appendChild(newFields);
    });

    document.getElementById('fields-container').addEventListener('click', function (event) {
        if (event.target.classList.contains('remove-btn')) {
            event.target.closest('.case-row').remove();
        }
    });
});



