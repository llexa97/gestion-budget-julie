// JavaScript principal pour l'application de gestion de budget

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide flash messages après 5 secondes
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            message.style.opacity = '0';
            setTimeout(function() {
                message.remove();
            }, 300);
        }, 5000);
    });

    // Confirmation avant suppression
    const deleteButtons = document.querySelectorAll('.btn-danger');
    deleteButtons.forEach(function(button) {
        if (button.type === 'submit' && !button.hasAttribute('onclick')) {
            button.addEventListener('click', function(e) {
                if (!confirm('Êtes-vous sûr de vouloir supprimer cet élément ?')) {
                    e.preventDefault();
                }
            });
        }
    });

    // Validation du formulaire de transaction
    const transactionForm = document.querySelector('.form');
    if (transactionForm) {
        transactionForm.addEventListener('submit', function(e) {
            const amountInput = document.querySelector('input[name="amount"]');
            if (amountInput) {
                const amount = parseFloat(amountInput.value);
                if (isNaN(amount) || amount < 0) {
                    e.preventDefault();
                    alert('Le montant doit être supérieur ou égal à 0');
                }
            }
        });
    }

    // Gérer le changement visuel instantané lors du clic sur un type de transaction
    const radioInputs = document.querySelectorAll('input[name="type"]');
    const typeLabels = document.querySelectorAll('label[class*="cursor-pointer"]');

    radioInputs.forEach((radio, index) => {
        radio.addEventListener('change', function() {
            // Réinitialiser tous les labels et spans
            typeLabels.forEach(label => {
                label.className = 'relative flex cursor-pointer rounded-lg border-2 border-gray-300 bg-white hover:bg-gray-50 hover:border-gray-400 p-4 focus:outline-none transition-all duration-200 transform';
                const span = label.querySelector('span');
                if (span) span.className = 'text-sm font-medium text-gray-900';
            });

            // Appliquer le style au label sélectionné
            const selectedLabel = typeLabels[index];
            const value = radio.value;

            if (value === 'ENTREE') {
                selectedLabel.className = 'relative flex cursor-pointer rounded-lg border-2 border-green-500 bg-green-50 shadow-lg scale-105 p-4 focus:outline-none transition-all duration-200 transform';
                selectedLabel.querySelector('span').className = 'text-sm font-medium text-green-700';
            } else if (value === 'DEPENSE') {
                selectedLabel.className = 'relative flex cursor-pointer rounded-lg border-2 border-red-500 bg-red-50 shadow-lg scale-105 p-4 focus:outline-none transition-all duration-200 transform';
                selectedLabel.querySelector('span').className = 'text-sm font-medium text-red-700';
            } else {
                selectedLabel.className = 'relative flex cursor-pointer rounded-lg border-2 border-yellow-500 bg-yellow-50 shadow-lg scale-105 p-4 focus:outline-none transition-all duration-200 transform';
                selectedLabel.querySelector('span').className = 'text-sm font-medium text-yellow-700';
            }
        });
    });

    // Formatage automatique des montants
    const amountInputs = document.querySelectorAll('input[type="number"][step="0.01"]');
    amountInputs.forEach(function(input) {
        input.addEventListener('blur', function() {
            if (this.value) {
                this.value = parseFloat(this.value).toFixed(2);
            }
        });
    });
});
