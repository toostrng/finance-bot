// Mobile Finance Manager Web App JavaScript

class FinanceManager {
    constructor() {
        this.userId = null;
        this.userData = null;
        this.currentPage = 'dashboard-page';
        this.charts = {};
        
        this.init();
    }

    async init() {
        // Get user ID from URL or Telegram WebApp
        this.userId = this.getUserId();
        
        if (!this.userId) {
            this.showError('User ID not found');
            return;
        }

        // Initialize user data
        await this.loadUserData();
        
        // Initialize UI
        this.initUI();
        
        // Load initial data
        await this.loadDashboardData();
        
        // Hide loading screen
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('app').classList.remove('hidden');
    }

    getUserId() {
        // Try to get from Telegram WebApp
        if (window.Telegram && window.Telegram.WebApp) {
            return window.Telegram.WebApp.initDataUnsafe?.user?.id;
        }
        
        // Try to get from URL parameters
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get('user_id') || urlParams.get('userId');
    }

    async loadUserData() {
        try {
            const response = await fetch(`/api/user/${this.userId}`);
            if (response.ok) {
                this.userData = await response.json();
                document.getElementById('user-name').textContent = this.userData.first_name || 'Пользователь';
            } else {
                // Create user if not exists
                await this.createUser();
            }
        } catch (error) {
            console.error('Error loading user data:', error);
            this.showError('Failed to load user data');
        }
    }

    async createUser() {
        try {
            const userData = {
                username: window.Telegram?.WebApp?.initDataUnsafe?.user?.username,
                first_name: window.Telegram?.WebApp?.initDataUnsafe?.user?.first_name,
                last_name: window.Telegram?.WebApp?.initDataUnsafe?.user?.last_name
            };

            const response = await fetch(`/api/user/${this.userId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData)
            });

            if (response.ok) {
                this.userData = await response.json();
                document.getElementById('user-name').textContent = this.userData.first_name || 'Пользователь';
            }
        } catch (error) {
            console.error('Error creating user:', error);
        }
    }

    initUI() {
        // Bottom navigation
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const pageName = e.currentTarget.dataset.page;
                this.switchPage(pageName);
            });
        });

        // Modal close buttons
        document.querySelectorAll('.modal-close').forEach(btn => {
            btn.addEventListener('click', () => {
                this.closeAllModals();
            });
        });

        // Modal overlays
        document.querySelectorAll('.modal-overlay').forEach(overlay => {
            overlay.addEventListener('click', () => {
                this.closeAllModals();
            });
        });

        // Quick action buttons
        document.getElementById('add-income-btn').addEventListener('click', () => {
            this.openTransactionModal('income');
        });

        document.getElementById('add-expense-btn').addEventListener('click', () => {
            this.openTransactionModal('expense');
        });

        // Form submissions
        document.getElementById('transaction-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.submitTransaction();
        });

        document.getElementById('wallet-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.submitWallet();
        });

        document.getElementById('category-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.submitCategory();
        });

        document.getElementById('income-source-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.submitIncomeSource();
        });

        // Transaction type change
        document.getElementById('transaction-type').addEventListener('change', (e) => {
            this.toggleTransactionFields(e.target.value);
        });

        // Settings
        document.getElementById('settings-btn').addEventListener('click', () => {
            this.openSettingsModal();
        });

        document.getElementById('save-settings').addEventListener('click', () => {
            this.saveSettings();
        });

        // Page-specific buttons
        document.getElementById('add-transaction-btn').addEventListener('click', () => {
            this.openTransactionModal();
        });

        document.getElementById('add-wallet-modal-btn').addEventListener('click', () => {
            this.openWalletModal();
        });

        document.getElementById('add-category-btn').addEventListener('click', () => {
            this.openCategoryModal();
        });

        document.getElementById('add-income-source-btn').addEventListener('click', () => {
            this.openIncomeSourceModal();
        });

        // Transaction filter
        document.getElementById('transaction-filter').addEventListener('change', (e) => {
            this.filterTransactions(e.target.value);
        });
    }

    switchPage(pageName) {
        // Update navigation
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-page="${pageName}"]`).classList.add('active');

        // Update content
        document.querySelectorAll('.page').forEach(page => {
            page.classList.remove('active');
        });
        document.getElementById(pageName).classList.add('active');

        this.currentPage = pageName;

        // Load page-specific data
        switch (pageName) {
            case 'dashboard-page':
                this.loadDashboardData();
                break;
            case 'transactions-page':
                this.loadTransactions();
                break;
            case 'wallets-page':
                this.loadWallets();
                break;
            case 'categories-page':
                this.loadCategories();
                break;
            case 'income-sources-page':
                this.loadIncomeSources();
                break;
            case 'reports-page':
                this.loadReports();
                break;
        }
    }

    async loadDashboardData() {
        try {
            const response = await fetch(`/api/user/${this.userId}/summary`);
            if (response.ok) {
                const data = await response.json();
                this.updateDashboard(data);
            }
        } catch (error) {
            console.error('Error loading dashboard data:', error);
        }
    }

    updateDashboard(data) {
        const { summary, wallet_balances } = data;

        // Update summary cards
        document.getElementById('total-balance').textContent = this.formatCurrency(
            wallet_balances.reduce((sum, wallet) => sum + wallet.balance, 0),
            'BYN'
        );
        document.getElementById('monthly-income').textContent = this.formatCurrency(summary.total_income, 'BYN');
        document.getElementById('monthly-expenses').textContent = this.formatCurrency(summary.total_expense, 'BYN');
        document.getElementById('net-income').textContent = this.formatCurrency(summary.net_income, 'BYN');

        // Load recent transactions
        this.loadRecentTransactions();
    }

    async loadRecentTransactions() {
        try {
            const response = await fetch(`/api/user/${this.userId}/transactions?limit=5`);
            if (response.ok) {
                const transactions = await response.json();
                this.renderRecentTransactions(transactions);
            }
        } catch (error) {
            console.error('Error loading recent transactions:', error);
        }
    }

    renderRecentTransactions(transactions) {
        const container = document.getElementById('recent-transactions');
        
        if (transactions.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">📊</div>
                    <div class="empty-state-text">Нет транзакций</div>
                </div>
            `;
            return;
        }

        container.innerHTML = transactions.map(transaction => `
            <div class="transaction-card ${transaction.transaction_type}">
                <div class="flex items-center">
                    <div class="flex-shrink-0">
                        <div class="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center">
                            <i class="fas fa-${transaction.transaction_type === 'income' ? 'arrow-up text-green-600' : 'arrow-down text-red-600'}"></i>
                        </div>
                    </div>
                    <div class="ml-3 flex-1">
                        <div class="text-sm font-medium text-gray-900">
                            ${transaction.description || 'Без описания'}
                        </div>
                        <div class="text-xs text-gray-500">
                            ${transaction.wallet_name} • ${new Date(transaction.date).toLocaleDateString()}
                        </div>
                    </div>
                </div>
                <div class="transaction-amount ${transaction.transaction_type}">
                    ${transaction.transaction_type === 'income' ? '+' : '-'}${this.formatCurrency(transaction.amount, transaction.currency)}
                </div>
            </div>
        `).join('');
    }

    async loadTransactions() {
        try {
            const response = await fetch(`/api/user/${this.userId}/transactions`);
            if (response.ok) {
                const transactions = await response.json();
                this.renderTransactions(transactions);
            }
        } catch (error) {
            console.error('Error loading transactions:', error);
        }
    }

    renderTransactions(transactions) {
        const container = document.getElementById('transactions-list');
        
        if (transactions.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">📊</div>
                    <div class="empty-state-text">Нет транзакций</div>
                </div>
            `;
            return;
        }

        container.innerHTML = transactions.map(transaction => `
            <div class="transaction-card ${transaction.transaction_type}" data-id="${transaction.id}">
                <div class="flex items-center">
                    <div class="flex-shrink-0">
                        <div class="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center">
                            <i class="fas fa-${transaction.transaction_type === 'income' ? 'arrow-up text-green-600' : 'arrow-down text-red-600'}"></i>
                        </div>
                    </div>
                    <div class="ml-3 flex-1">
                        <div class="text-sm font-medium text-gray-900">
                            ${transaction.description || 'Без описания'}
                        </div>
                        <div class="text-xs text-gray-500">
                            ${transaction.wallet_name} • ${new Date(transaction.date).toLocaleDateString()}
                        </div>
                        ${transaction.income_source_name ? `<div class="text-xs text-gray-400">${transaction.income_source_name}</div>` : ''}
                        ${transaction.expense_category_name ? `<div class="text-xs text-gray-400">${transaction.expense_category_name}</div>` : ''}
                    </div>
                </div>
                <div class="flex items-center space-x-2">
                    <div class="transaction-amount ${transaction.transaction_type}">
                        ${transaction.transaction_type === 'income' ? '+' : '-'}${this.formatCurrency(transaction.amount, transaction.currency)}
                    </div>
                    <button class="text-gray-400 hover:text-red-600" onclick="app.deleteTransaction(${transaction.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `).join('');
    }

    async loadWallets() {
        try {
            const response = await fetch(`/api/user/${this.userId}/wallets`);
            if (response.ok) {
                const wallets = await response.json();
                this.renderWallets(wallets);
            }
        } catch (error) {
            console.error('Error loading wallets:', error);
        }
    }

    renderWallets(wallets) {
        const container = document.getElementById('wallets-list');
        
        if (wallets.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">💳</div>
                    <div class="empty-state-text">Нет кошельков</div>
                </div>
            `;
            return;
        }

        container.innerHTML = wallets.map(wallet => `
            <div class="wallet-card">
                <div class="flex items-center justify-between mb-3">
                    <h3 class="text-lg font-semibold text-gray-900">${wallet.name}</h3>
                    <button class="text-gray-400 hover:text-red-600" onclick="app.deleteWallet(${wallet.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
                <div class="wallet-balance">
                    ${this.formatCurrency(wallet.balance, wallet.currency)}
                </div>
                <div class="text-sm text-gray-500 mt-2">
                    Валюта: ${wallet.currency}
                </div>
            </div>
        `).join('');
    }

    async loadCategories() {
        try {
            const response = await fetch(`/api/user/${this.userId}/expense-categories`);
            if (response.ok) {
                const categories = await response.json();
                this.renderCategories(categories);
            }
        } catch (error) {
            console.error('Error loading categories:', error);
        }
    }

    renderCategories(categories) {
        const container = document.getElementById('categories-list');
        
        if (categories.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">🏷️</div>
                    <div class="empty-state-text">Нет категорий</div>
                </div>
            `;
            return;
        }

        container.innerHTML = categories.map(category => `
            <div class="category-card">
                <div class="flex items-center">
                    <span class="category-icon" style="color: ${category.color}">${category.icon}</span>
                    <div>
                        <h3 class="font-medium text-gray-900">${category.name}</h3>
                        ${category.description ? `<p class="text-sm text-gray-500">${category.description}</p>` : ''}
                    </div>
                </div>
                <button class="text-gray-400 hover:text-red-600" onclick="app.deleteCategory(${category.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `).join('');
    }

    async loadIncomeSources() {
        try {
            const response = await fetch(`/api/user/${this.userId}/income-sources`);
            if (response.ok) {
                const sources = await response.json();
                this.renderIncomeSources(sources);
            }
        } catch (error) {
            console.error('Error loading income sources:', error);
        }
    }

    renderIncomeSources(sources) {
        const container = document.getElementById('income-sources-list');
        
        if (sources.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">💰</div>
                    <div class="empty-state-text">Нет источников дохода</div>
                </div>
            `;
            return;
        }

        container.innerHTML = sources.map(source => `
            <div class="income-source-card">
                <div>
                    <h3 class="font-medium text-gray-900">${source.name}</h3>
                    ${source.description ? `<p class="text-sm text-gray-500">${source.description}</p>` : ''}
                </div>
                <button class="text-gray-400 hover:text-red-600" onclick="app.deleteIncomeSource(${source.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `).join('');
    }

    async loadReports() {
        try {
            const response = await fetch(`/api/user/${this.userId}/summary?period=30`);
            if (response.ok) {
                const data = await response.json();
                this.renderReports(data.summary);
            }
        } catch (error) {
            console.error('Error loading reports:', error);
        }
    }

    renderReports(summary) {
        // Expense by category chart
        const expenseCtx = document.getElementById('expense-chart').getContext('2d');
        if (this.charts.expense) {
            this.charts.expense.destroy();
        }
        
        const expenseLabels = Object.keys(summary.expenses_by_category);
        const expenseData = Object.values(summary.expenses_by_category);
        
        this.charts.expense = new Chart(expenseCtx, {
            type: 'doughnut',
            data: {
                labels: expenseLabels,
                datasets: [{
                    data: expenseData,
                    backgroundColor: [
                        '#3B82F6', '#EF4444', '#10B981', '#F59E0B', '#8B5CF6',
                        '#06B6D4', '#84CC16', '#F97316', '#EC4899', '#6366F1'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            font: {
                                size: 12
                            }
                        }
                    }
                }
            }
        });

        // Income by source chart
        const incomeCtx = document.getElementById('income-chart').getContext('2d');
        if (this.charts.income) {
            this.charts.income.destroy();
        }
        
        const incomeLabels = Object.keys(summary.income_by_source);
        const incomeData = Object.values(summary.income_by_source);
        
        this.charts.income = new Chart(incomeCtx, {
            type: 'doughnut',
            data: {
                labels: incomeLabels,
                datasets: [{
                    data: incomeData,
                    backgroundColor: [
                        '#10B981', '#3B82F6', '#F59E0B', '#EF4444', '#8B5CF6',
                        '#06B6D4', '#84CC16', '#F97316', '#EC4899', '#6366F1'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            font: {
                                size: 12
                            }
                        }
                    }
                }
            }
        });
    }

    // Modal functions
    openTransactionModal(type = null) {
        this.loadWalletsForSelect();
        this.loadIncomeSourcesForSelect();
        this.loadCategoriesForSelect();
        
        if (type) {
            document.getElementById('transaction-type').value = type;
            this.toggleTransactionFields(type);
        }
        
        document.getElementById('transaction-modal').classList.remove('hidden');
        document.getElementById('transaction-date').value = new Date().toISOString().slice(0, 16);
    }

    openWalletModal() {
        document.getElementById('wallet-modal').classList.remove('hidden');
    }

    openCategoryModal() {
        document.getElementById('category-modal').classList.remove('hidden');
    }

    openIncomeSourceModal() {
        document.getElementById('income-source-modal').classList.remove('hidden');
    }

    openSettingsModal() {
        document.getElementById('default-currency').value = this.userData?.default_currency || 'BYN';
        document.getElementById('settings-modal').classList.remove('hidden');
    }

    closeAllModals() {
        document.querySelectorAll('.modal').forEach(modal => {
            modal.classList.add('hidden');
        });
    }

    toggleTransactionFields(type) {
        const incomeField = document.getElementById('income-source-field');
        const expenseField = document.getElementById('expense-category-field');
        
        if (type === 'income') {
            incomeField.classList.remove('hidden');
            expenseField.classList.add('hidden');
        } else {
            incomeField.classList.add('hidden');
            expenseField.classList.remove('hidden');
        }
    }

    // Form submission functions
    async submitTransaction() {
        const formData = {
            wallet_id: parseInt(document.getElementById('transaction-wallet').value),
            transaction_type: document.getElementById('transaction-type').value,
            amount: parseFloat(document.getElementById('transaction-amount').value),
            currency: document.getElementById('transaction-currency').value,
            description: document.getElementById('transaction-description').value,
            date: document.getElementById('transaction-date').value,
            income_source_id: document.getElementById('transaction-income-source').value || null,
            expense_category_id: document.getElementById('transaction-expense-category').value || null
        };

        try {
            const response = await fetch(`/api/user/${this.userId}/transactions`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                this.closeAllModals();
                this.showSuccess('Транзакция добавлена');
                this.loadDashboardData();
                if (this.currentPage === 'transactions-page') {
                    this.loadTransactions();
                }
            } else {
                this.showError('Ошибка при добавлении транзакции');
            }
        } catch (error) {
            console.error('Error submitting transaction:', error);
            this.showError('Ошибка при добавлении транзакции');
        }
    }

    async submitWallet() {
        const formData = {
            name: document.getElementById('wallet-name').value,
            currency: document.getElementById('wallet-currency').value
        };

        try {
            const response = await fetch(`/api/user/${this.userId}/wallets`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                this.closeAllModals();
                this.showSuccess('Кошелек добавлен');
                this.loadWallets();
            } else {
                this.showError('Ошибка при добавлении кошелька');
            }
        } catch (error) {
            console.error('Error submitting wallet:', error);
            this.showError('Ошибка при добавлении кошелька');
        }
    }

    async submitCategory() {
        const formData = {
            name: document.getElementById('category-name').value,
            description: document.getElementById('category-description').value,
            color: document.getElementById('category-color').value,
            icon: document.getElementById('category-icon').value
        };

        try {
            const response = await fetch(`/api/user/${this.userId}/expense-categories`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                this.closeAllModals();
                this.showSuccess('Категория добавлена');
                this.loadCategories();
            } else {
                this.showError('Ошибка при добавлении категории');
            }
        } catch (error) {
            console.error('Error submitting category:', error);
            this.showError('Ошибка при добавлении категории');
        }
    }

    async submitIncomeSource() {
        const formData = {
            name: document.getElementById('income-source-name').value,
            description: document.getElementById('income-source-description').value
        };

        try {
            const response = await fetch(`/api/user/${this.userId}/income-sources`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                this.closeAllModals();
                this.showSuccess('Источник дохода добавлен');
                this.loadIncomeSources();
            } else {
                this.showError('Ошибка при добавлении источника дохода');
            }
        } catch (error) {
            console.error('Error submitting income source:', error);
            this.showError('Ошибка при добавлении источника дохода');
        }
    }

    async saveSettings() {
        const currency = document.getElementById('default-currency').value;

        try {
            const response = await fetch(`/api/user/${this.userId}/currency`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ currency })
            });

            if (response.ok) {
                this.closeAllModals();
                this.showSuccess('Настройки сохранены');
                this.userData.default_currency = currency;
            } else {
                this.showError('Ошибка при сохранении настроек');
            }
        } catch (error) {
            console.error('Error saving settings:', error);
            this.showError('Ошибка при сохранении настроек');
        }
    }

    // Load data for select fields
    async loadWalletsForSelect() {
        try {
            const response = await fetch(`/api/user/${this.userId}/wallets`);
            if (response.ok) {
                const wallets = await response.json();
                const select = document.getElementById('transaction-wallet');
                select.innerHTML = wallets.map(wallet => 
                    `<option value="${wallet.id}">${wallet.name} (${wallet.currency})</option>`
                ).join('');
            }
        } catch (error) {
            console.error('Error loading wallets for select:', error);
        }
    }

    async loadIncomeSourcesForSelect() {
        try {
            const response = await fetch(`/api/user/${this.userId}/income-sources`);
            if (response.ok) {
                const sources = await response.json();
                const select = document.getElementById('transaction-income-source');
                select.innerHTML = '<option value="">Выберите источник</option>' + 
                    sources.map(source => 
                        `<option value="${source.id}">${source.name}</option>`
                    ).join('');
            }
        } catch (error) {
            console.error('Error loading income sources for select:', error);
        }
    }

    async loadCategoriesForSelect() {
        try {
            const response = await fetch(`/api/user/${this.userId}/expense-categories`);
            if (response.ok) {
                const categories = await response.json();
                const select = document.getElementById('transaction-expense-category');
                select.innerHTML = '<option value="">Выберите категорию</option>' + 
                    categories.map(category => 
                        `<option value="${category.id}">${category.name}</option>`
                    ).join('');
            }
        } catch (error) {
            console.error('Error loading categories for select:', error);
        }
    }

    // Delete functions
    async deleteTransaction(id) {
        if (!confirm('Удалить транзакцию?')) return;

        try {
            const response = await fetch(`/api/user/${this.userId}/transactions/${id}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                this.showSuccess('Транзакция удалена');
                this.loadDashboardData();
                if (this.currentPage === 'transactions-page') {
                    this.loadTransactions();
                }
            } else {
                this.showError('Ошибка при удалении транзакции');
            }
        } catch (error) {
            console.error('Error deleting transaction:', error);
            this.showError('Ошибка при удалении транзакции');
        }
    }

    async deleteWallet(id) {
        if (!confirm('Удалить кошелек?')) return;

        try {
            const response = await fetch(`/api/user/${this.userId}/wallets/${id}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                this.showSuccess('Кошелек удален');
                this.loadWallets();
            } else {
                this.showError('Ошибка при удалении кошелька');
            }
        } catch (error) {
            console.error('Error deleting wallet:', error);
            this.showError('Ошибка при удалении кошелька');
        }
    }

    async deleteCategory(id) {
        if (!confirm('Удалить категорию?')) return;

        try {
            const response = await fetch(`/api/user/${this.userId}/expense-categories/${id}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                this.showSuccess('Категория удалена');
                this.loadCategories();
            } else {
                this.showError('Ошибка при удалении категории');
            }
        } catch (error) {
            console.error('Error deleting category:', error);
            this.showError('Ошибка при удалении категории');
        }
    }

    async deleteIncomeSource(id) {
        if (!confirm('Удалить источник дохода?')) return;

        try {
            const response = await fetch(`/api/user/${this.userId}/income-sources/${id}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                this.showSuccess('Источник дохода удален');
                this.loadIncomeSources();
            } else {
                this.showError('Ошибка при удалении источника дохода');
            }
        } catch (error) {
            console.error('Error deleting income source:', error);
            this.showError('Ошибка при удалении источника дохода');
        }
    }

    // Utility functions
    formatCurrency(amount, currency) {
        return new Intl.NumberFormat('ru-RU', {
            style: 'currency',
            currency: currency
        }).format(amount);
    }

    filterTransactions(filter) {
        const cards = document.querySelectorAll('.transaction-card');
        cards.forEach(card => {
            if (filter === 'all' || card.classList.contains(filter)) {
                card.style.display = 'flex';
            } else {
                card.style.display = 'none';
            }
        });
    }

    showSuccess(message) {
        this.showMessage(message, 'success');
    }

    showError(message) {
        this.showMessage(message, 'error');
    }

    showMessage(message, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message message-${type} fixed top-4 right-4 z-50`;
        messageDiv.textContent = message;
        
        document.body.appendChild(messageDiv);
        
        setTimeout(() => {
            messageDiv.remove();
        }, 3000);
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new FinanceManager();
}); 