   let captchaVerified = false;
        let termsAccepted = false;

        // Alternar visibilidade da senha
        function togglePassword(fieldId) {
            const passwordInput = document.getElementById(fieldId);
            const icon = passwordInput.nextElementSibling;
            
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                icon.textContent = '🔓';
            } else {
                passwordInput.type = 'password';
                icon.textContent = '🔒';
            }
        }

        // Verificar força da senha
        function checkPasswordStrength(password) {
            const strengthBar = document.getElementById('strengthBar');
            const strengthText = document.getElementById('strengthText');
            
            let score = 0;
            if (password.length >= 8) score++;
            if (password.match(/[a-z]/)) score++;
            if (password.match(/[A-Z]/)) score++;
            if (password.match(/[0-9]/)) score++;
            if (password.match(/[^a-zA-Z0-9]/)) score++;

            strengthBar.className = 'strength-fill';
            
            if (score < 3) {
                strengthBar.classList.add('strength-weak');
                strengthText.textContent = 'Senha fraca';
                strengthText.style.color = '#e53e3e';
            } else if (score < 5) {
                strengthBar.classList.add('strength-medium');
                strengthText.textContent = 'Senha média';
                strengthText.style.color = '#ed8936';
            } else {
                strengthBar.classList.add('strength-strong');
                strengthText.textContent = 'Senha forte';
                strengthText.style.color = '#38a169';
            }
        }

        // Verificar CAPTCHA
        function verifyCaptcha() {
            const captchaBox = document.getElementById('captchaBox');
            
            if (captchaVerified) return;
            
            captchaBox.classList.add('loading');
            
            setTimeout(() => {
                captchaBox.classList.remove('loading');
                captchaBox.classList.add('verified');
                captchaBox.innerHTML = '✓';
                captchaVerified = true;
                updateSubmitButton();
            }, 2000);
        }

        // Alternar checkbox
        function toggleCheckbox(id) {
            const checkbox = document.getElementById(id);
            const isChecked = checkbox.classList.contains('checked');
            
            if (isChecked) {
                checkbox.classList.remove('checked');
                checkbox.innerHTML = '';
                if (id === 'termsCheck') termsAccepted = false;
            } else {
                checkbox.classList.add('checked');
                checkbox.innerHTML = '✓';
                if (id === 'termsCheck') termsAccepted = true;
            }
            
            updateSubmitButton();
        }

        // Atualizar estado do botão de submit
        function updateSubmitButton() {
            const registerButton = document.getElementById('registerButton');
            registerButton.disabled = !(captchaVerified && termsAccepted);
        }

        // Validar confirmação de senha
        function validatePasswordMatch() {
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirmPassword').value;
            const errorDiv = document.getElementById('confirmPasswordError');
            
            if (confirmPassword && password !== confirmPassword) {
                errorDiv.textContent = 'As senhas não coincidem';
                errorDiv.style.display = 'block';
                return false;
            } else {
                errorDiv.style.display = 'none';
                return true;
            }
        }

        // Event listeners
        document.getElementById('password').addEventListener('input', function() {
            checkPasswordStrength(this.value);
        });

        document.getElementById('confirmPassword').addEventListener('input', validatePasswordMatch);

        document.getElementById('age').addEventListener('input', function() {
            const age = parseInt(this.value);
            const errorDiv = document.getElementById('ageError');
            
            if (age && (age < 16 || age > 100)) {
                errorDiv.textContent = 'Idade deve estar entre 16 e 100 anos';
                errorDiv.style.display = 'block';
            } else {
                errorDiv.style.display = 'none';
            }
        });

        // Validação e máscara para e-mail ou telefone
        document.getElementById('emailPhone').addEventListener('input', function() {
            const value = this.value;
            const icon = this.nextElementSibling;
            const errorDiv = document.getElementById('emailPhoneError');
            
            // Detectar se é e-mail ou telefone
            if (value.includes('@')) {
                icon.textContent = '📧';
                // Validação simples de e-mail
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (value.length > 0 && !emailRegex.test(value)) {
                    errorDiv.textContent = 'Digite um e-mail válido';
                    errorDiv.style.display = 'block';
                } else {
                    errorDiv.style.display = 'none';
                }
            } else if (value.match(/^\d/)) {
                icon.textContent = '📱';
                // Aplicar máscara de telefone
                let cleanValue = value.replace(/\D/g, '');
                if (cleanValue.length >= 11) {
                    cleanValue = cleanValue.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
                } else if (cleanValue.length >= 7) {
                    cleanValue = cleanValue.replace(/(\d{2})(\d{4})(\d{0,4})/, '($1) $2-$3');
                } else if (cleanValue.length >= 3) {
                    cleanValue = cleanValue.replace(/(\d{2})(\d{0,5})/, '($1) $2');
                }
                this.value = cleanValue;
                
                // Validação de telefone
                if (cleanValue.length > 0 && cleanValue.replace(/\D/g, '').length < 10) {
                    errorDiv.textContent = 'Digite um telefone válido';
                    errorDiv.style.display = 'block';
                } else {
                    errorDiv.style.display = 'none';
                }
            } else {
                icon.textContent = '👤';
                errorDiv.style.display = 'none';
            }
        });

        // Funções auxiliares
        function showTerms() {
            alert('Aqui seriam exibidos os Termos de Uso da academia.');
        }

        function showPrivacy() {
            alert('Aqui seria exibida a Política de Privacidade.');
        }

        function showLogin() {
            alert('Redirecionando para a página de login...');
        }

        // Validação do formulário
        document.getElementById('registerForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const firstName = document.getElementById('firstName').value;
            const emailPhone = document.getElementById('emailPhone').value;
            const password = document.getElementById('password').value;
            const age = document.getElementById('age').value;
            
            if (!firstName || !emailPhone || !password || !age || !termsAccepted || !captchaVerified) {
                document.querySelector('.register-container').classList.add('shake');
                setTimeout(() => {
                    document.querySelector('.register-container').classList.remove('shake');
                }, 500);
                return;
            }
            
            if (!validatePasswordMatch()) {
                return;
            }
            
            // Simulação de cadastro
            const btn = document.getElementById('registerButton');
            btn.textContent = 'Criando conta...';
            btn.style.background = '#a0aec0';
            
            setTimeout(() => {
                alert('Conta criada com sucesso!\n\nVerifique seu e-mail para confirmar sua conta.');
                btn.textContent = 'Criar Conta';
                btn.style.background = 'linear-gradient(135deg, #667eea, #764ba2)';
            }, 3000);
        });
