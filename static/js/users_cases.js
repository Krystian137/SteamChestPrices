document.addEventListener("DOMContentLoaded", function () {
    const addToTableButton = document.getElementById("add_button");
    const addFieldButton = document.getElementById("one_more_chest");
    const fieldsContainer = document.getElementById("fields-container");
    const tableBody = document.getElementById("priceTableBody");

    if (addFieldButton) {
        addFieldButton.addEventListener("click", function () {
            const firstField = fieldsContainer.querySelector(".case-row");
            if (firstField) {
                const newField = firstField.cloneNode(true);

                newField.querySelector("select[name='case_code[]']").selectedIndex = 0;
                newField.querySelector("input[name='quantity[]']").value = "";
                addRemoveEvent(newField);
                fieldsContainer.appendChild(newField);
            }
        });
    }

    if (addToTableButton) {
        addToTableButton.addEventListener("click", function (event) {
            event.preventDefault();

            const rows = fieldsContainer.querySelectorAll(".case-row");

            rows.forEach(row => {
                const caseCode = row.querySelector("select[name='case_code[]']").value;
                const quantity = row.querySelector("input[name='quantity[]']").value;

                if (caseCode.trim() !== "" && quantity.trim() !== "") {
                    const newRow = document.createElement("tr");

                    const caseCell = document.createElement("td");
                    caseCell.textContent = caseCode;

                    const quantityCell = document.createElement("td");
                    quantityCell.textContent = quantity;

                    const removeCell = document.createElement("td");
                    const removeButton = document.createElement("button");
                    removeButton.textContent = "Usuń";
                    removeButton.classList.add("btn", "btn-danger", "btn-sm");
                    removeButton.addEventListener("click", function () {
                        newRow.remove();
                    });

                    removeCell.appendChild(removeButton);
                    newRow.appendChild(caseCell);
                    newRow.appendChild(quantityCell);
                    newRow.appendChild(removeCell);

                    tableBody.appendChild(newRow);
                }
            });
        });
    }

    function addRemoveEvent(element) {
        const removeButton = element.querySelector(".remove-btn");
        if (removeButton) {
            removeButton.addEventListener("click", function () {
                element.remove();
            });
        }
    }

    document.querySelectorAll(".case-row").forEach(addRemoveEvent);
});


document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".delete-btn").forEach(button => {
        button.addEventListener("click", function () {
            if (!confirm("Czy na pewno chcesz usunąć tę skrzynię?")) return;
            fetch(this.dataset.url, { method: "POST" })
                .then(response => response.text())
                .then(() => location.reload());
        });
    });

    document.querySelectorAll(".edit-form").forEach(form => {
        form.addEventListener("submit", function (event) {
            event.preventDefault();
            fetch(this.action, {
                method: "POST",
                body: new FormData(this)
            }).then(response => response.text())
              .then(() => location.reload());
        });
    });
});
