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
                if (isNaN(amount) || amount <= 0) {
                    e.preventDefault();
                    alert('Le montant doit être supérieur à 0');
                }
            }
        });
    }

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
