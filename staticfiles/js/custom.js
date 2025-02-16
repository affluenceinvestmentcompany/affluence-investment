document.addEventListener('DOMContentLoaded', function () {
    (function ($) {
        "use strict";

        // Header Type = Fixed
        $(window).scroll(function () {
            var scroll = $(window).scrollTop();
            var box = $('.header-text').height();
            var header = $('header').height();

            if (scroll >= box - header) {
                $("header").addClass("background-header");
            } else {
                $("header").removeClass("background-header");
            }
        });

        // Page loading animation
        $(window).on('load', function () {
            $('#js-preloader').addClass('loaded');
        });

        $(document).on('click', '.modal_trigger', function() {
            $(this).leanModal({
                top: 100,
                overlay: 0.7,
                closeButton: ".modal_close"
            });
        });
        

        // $(".modal_trigger").leanModal({
        //     top: 100,
        //     overlay: 0.7,
        //     closeButton: ".modal_close"
        // });
        $(".forgot-password-btn").leanModal({
            top: 100,
            overlay: 0.7,
            closeButton: ".modal_close1"
        });
        $(".show_ver_email").leanModal({
            top: 100,
            overlay: 0.7,
            closeButton: ".modal_close2"
        });
        $(".add-payment-btn").leanModal({
            top: 100,
            overlay: 0.7,
            closeButton: ".modal_close6"
        });
        $(".add-user-btn").leanModal({
            top: 100,
            overlay: 0.7,
            closeButton: ".modal_close3"
        });
        $(".goto_signin2").leanModal({
            top: 100,
            overlay: 0.7,
            closeButton: ".modal_close3"
        });
        $(".add-payment-btn").leanModal({
            top: 100,
            overlay: 0.7,
            closeButton: ".modal_close6"
        });
        $(".add-user-btn").leanModal({
            top: 100,
            overlay: 0.7,
            closeButton: ".modal_close3"
        });


        $('.modal_trigger').on('click', function () {
            $(".closeModal").click();
        });

        $('.show_ver_email').on('click', function () {
            $(".closeModal").click();
        });

        $(".modal_close1").click(function () {
            $('#lean_overlay2').css({
                'display': 'none',
            });
        });

        $(".goto_signin2").click(function () {
            $(".modal_close1").click();
            $('#lean_overlay2').css({
                'display': 'block',
            });
        });

        $(".modal_close2").click(function () {
            $('#lean_overlay2').css({
                'display': 'none',
            });
        });

        $('#dashboardLink').on('click', function () {
            localStorage.removeItem('activeNavLink')
        })

        $(".gsba").hide();
        $(function () {
            // Calling Login Form
            $("#login_form").click(function () {
                $(".popupHeader").addClass('disable');
                $(".reg_login_nav").hide();
                $(".user_login").show();
                $(".gsba").show();
                return false;
            });
            $(".goto_signin").click(function () {
                $(".popupHeader").addClass('disable');
                $(".reg_login_nav").hide();
                $(".user_register").hide();
                $(".forgot_password").hide();
                $(".user_login").show();
                $(".gsba").show();
                return false;
            });

            // Calling Register Form
            $("#register_form").click(function () {
                $(".popupHeader").addClass('disable');
                $(".reg_login_nav").hide();
                $(".user_register").show();
                $(".gsba").show();
                return false;
            });
            $(".goto_signup").click(function () {
                $(".popupHeader").addClass('disable');
                $(".reg_login_nav").hide();
                $(".user_login").hide();
                $(".forgot_password").hide();
                $(".user_register").show();
                $(".gsba").show();
                // $(".header_title").text('Sign Up');
                return false;
            });

            // Calling Forgot password
            $(".forgot-password-btn").click(function () {
                $(".popupHeader").addClass('disable');
                $(".modal_close").click();
                $('#lean_overlay2').css({
                    'display': 'block',
                });
                $(".gsba").show();
                return false;
            });

            // Going back to Social Forms
            // $(".back_btn").click(function () {
            //     $(".user_login").hide();
            //     $(".user_register").hide();
            //     $(".forgot_password").hide();
            //     $(".reg_login_nav").show();
            //     $(".gsba").hide();
            //     $(".header_title").text('Sign Up \n|| Sign In');
            //     return false;
            // });
        });

        if ($('.menu-trigger').length) {
            $(".menu-trigger").on('click', function () {
                $(this).toggleClass('active');
                $('.nav').toggleClass('active');
            });
        }

        $("#sidebar_trigger").on('click', function () {
            $(this).hide();
            $('.sidebar').addClass('active');
            $('#sidebar_trigger2').addClass('active');
        });

        $("#sidebar_trigger2").on('click', function () {
            $(this).removeClass('active');
            $('#sidebar_trigger').show();
            $('.sidebar').removeClass('active');
        });

        $(document).click(function (e) {
            if (!$(e.target).closest('.main-nav').length) {
                $('.menu-trigger').removeClass('active');
                $('.nav').removeClass('active');
            }
            if (!$(e.target).closest('.dashboard').length) {
                $('.sidebar').removeClass('active');
                $('#sidebar_trigger').show();
                $('#sidebar_trigger2').removeClass('active');
            }

            if (!$(e.target).closest('.packages-table').length) {
                $('.edit-package-form').hide();
                $('#lean_overlay2').css({
                    'display': 'none',
                });
            }
        });

        $('.nav a').on('click', function () {
            $('.menu-trigger').removeClass('active');
            $('.nav').removeClass('active');
        });

        // Function to refresh
        function refreshSection(element) {
            let selector = element.startsWith('#') ? element : '.' + element;
            $(selector).load(location.href + ' ' + selector + ' > *', function() {
                console.log('Refreshed ' + element);
            });
        }

        // Hide/Show Password
        document.querySelectorAll('.togglePassword').forEach(function (button) {
            button.addEventListener('click', function () {
                let passwordFields = document.querySelectorAll('.password');

                passwordFields.forEach(function (passwordField) {
                    if (passwordField.type === "password") {
                        passwordField.type = "text";
                        $('.fa-eye').hide();
                        $('.fa-eye-slash').show();
                    } else {
                        passwordField.type = "password";
                        $('.fa-eye').show();
                        $('.fa-eye-slash').hide();
                    }
                });
            });
        });

        // Validate Email
        const validateEmail = (email) => {
            return email.match(
                /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
            )
        }
        let regex = new RegExp('^(?=.*[0-9])(?=.{8,})')

        // Remove non-digit
        document.querySelectorAll('.phone-input').forEach(function (input) {
            input.addEventListener('input', function () {
                let formattedNumber = input.value.replace(/\D/g, '');
                input.value = formattedNumber;
            });
        });

        document.querySelectorAll('.phone-input2').forEach(function (input) {
            input.addEventListener('input', function () {
                let formattedNumber = input.value.replace(/[^0-9.]/g, '');  
                if (formattedNumber.indexOf('.') !== formattedNumber.lastIndexOf('.')) {
                    formattedNumber = formattedNumber.substring(0, formattedNumber.lastIndexOf('.'));
                }
                input.value = formattedNumber;
            });
        });

        // =============== REGISTER AJAX===================
        $(document).on('click', '#regBtn', function (e) {
            e.preventDefault()
            var button = this;
            var full_name = $('input[name=full_name]').val()
            var email = $('input[name=email]').val()
            var phone = $('input[name=phone]').val()
            var password = $('input[name=password]').val()
            var password2 = $('input[name=password2]').val()
            var token = $('input[name=csrfmiddlewaretoken]').val()

            if (full_name == "" || full_name.length < 3) {
                document.getElementById('fnerr').innerHTML = 'Enter your full name'
                return false
            } else {
                document.getElementById('fnerr').innerHTML = "."
            }
            if (email == "" || !validateEmail(email)) {
                document.getElementById('emerr').innerHTML = 'Enter a valid email'
                return false
            } else {
                document.getElementById('emerr').innerHTML = "."
            }
            const phoneRegex = /^(?:\+?\d{1,3})?[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,4}$/;
            const isValidPhone = phoneRegex.test(phone);
            if (phone == "" || !isValidPhone) {
                document.getElementById('pherr').innerHTML = 'Enter a valid phone number'
                return false
            } else {
                document.getElementById('pherr').innerHTML = "."
            }
            if (password == "" || !regex.test(password)) {
                document.getElementById('pwderr').innerHTML = 'Minimum of 8 alphabets & numbers'
                return false
            } else {
                document.getElementById('pwderr').innerHTML = "."
            }
            if (password2 !== password) {
                document.getElementById('pwderr2').innerHTML = 'Password do not match'
                return false
            } else {
                document.getElementById('pwderr2').innerHTML = "."
            }

            showSpinner(button);

            $.ajax({
                method: 'POST',
                url: '/account/register/',
                data: {
                    'full_name': full_name, 'email': email, 'phone': phone, 'password': password,
                    csrfmiddlewaretoken: token
                },
                success: function (response) {
                    if (response.success) {
                        alertify.success(response.success)
                        window.location.reload();
                    } else if (response.error == 'Email already exist, try login...') {
                        document.getElementById('emerr').innerHTML = 'Email already exist, try login...'
                        return false;
                    } else {
                        alertify.error('An error occurred...')
                        return false;
                    }
                },
                error: function () {
                    alertify.error('An error occurred!');
                },
                complete: function() {
                    hideSpinner(button);
                }
            })
        })

        // =============LOGIN AJAX===============
        $(document).on('click', '#loginBtn', function (e) {
            e.preventDefault()
            var button = this;
            var email = $('input[name=login_email]').val()
            var password = $('input[name=login_password]').val()
            var token = $('input[name=csrfmiddlewaretoken]').val()

            if (email == "" || !validateEmail(email)) {
                document.getElementById('login_emerr').innerHTML = 'Enter a valid email'
                return false
            } else {
                document.getElementById('login_emerr').innerHTML = "."
            }
            if (password == "") {
                document.getElementById('login_pwderr').innerHTML = 'Enter your password'
                return false
            } else {
                document.getElementById('login_pwderr').innerHTML = "."
            }

            document.getElementById('invaliderr').innerHTML = '';

            showSpinner(button);

            $.ajax({
                method: 'POST',
                url: '/account/login/',
                data: {
                    'email': email, 'password': password,
                    csrfmiddlewaretoken: token
                },
                success: function (response) {
                    if (response.success) {
                        alertify.success(response.success);
                        window.location.reload();
                    } else if (response.error == 'Invalid email or password') {
                        document.getElementById('invaliderr').innerHTML = 'Invalid login details'
                        return false;
                    } else {
                        alertify.error(response.error)
                        return false;
                    }
                },
                error: function () {
                    alertify.error('An error occurred!');
                },
                complete: function() {
                    hideSpinner(button);
                }
            })
        })

        // =============LOGOUT AJAX===============
        $(document).on('click', '.logout', function (e) {
            e.preventDefault()
            var token = $('input[name=csrfmiddlewaretoken]').val();

            $('.logout-spinner').removeClass('d-none');
            $('.logout_form').addClass('d-none')

            $.ajax({
                method: 'POST',
                url: '/account/logout/',
                headers: {
                    'X-CSRFToken': token
                },
                success: function (response) {
                    if (response.success == 'Logout successful') {
                        alertify.success(response.success);
                        localStorage.clear();
                        window.location.href = '/';
                    } else {
                        alertify.error(response.error);
                        $('.logout-spinner').removeClass('d-none');
                        $('.logout_form').addClass('d-none');
                        return false;
                    }
                },
                error: function (xhr, status, error) {
                    console.log('AJAX Error:', error);
                    alertify.error('Logout failed');
                    $('.logout-spinner').addClass('d-none');
                    $('.logout_form').removeClass('d-none');
                }
            });
        })

        // =============RESEND EMAIL===============
        $(document).on('click', '#resendEmailBtn', function () {
            let button = this;
            let token = $('input[name=csrfmiddlewaretoken]').val();
            
            showSpinner(button);
            
            $.ajax({
                method: 'POST',
                url: '/account/resend-link/',
                data: { csrfmiddlewaretoken: token },
                success: function (response) {
                    if (response.success) {
                        alertify.success(response.success);
                        $(".modal_close2").click();
                    } else {
                        alertify.error(response.error);
                    }
                },
                error: function () {
                    alertify.error('An error occurred!');
                },
                complete: function() {
                    hideSpinner(button);
                }
            });
        });

        // =============FORGOT PASSWORD AJAX===============
        $(document).on('click', '#forgotPasswordBtn', function (e) {
            e.preventDefault();
            var button = this;
            var email = $('input[name=forgot_pass_email]').val()
            var token = $('input[name=csrfmiddlewaretoken]').val()

            if (email == "" || !validateEmail(email)) {
                document.getElementById('fp_emerr').innerHTML = 'Enter a valid email'
                return false
            } else {
                document.getElementById('fp_emerr').innerHTML = "."
            }

            showSpinner(button);

            $.ajax({
                method: 'POST',
                url: '/account/password_reset/',
                data: {
                    'email': email, csrfmiddlewaretoken: token
                },
                headers: {
                    'X-CSRFToken': token
                },
                success: function (response) {
                    if (response.success == 'Password reset email sent') {
                        alertify.success('Password reset email sent');
                        $(".modal_close1").click();
                        $(".modal_close").click();
                        $('#lean_overlay2').css({
                            'display': 'none',
                        });
                        $('#forgot-password-form')[0].reset();
                    } else if (response.error == 'Email is not registered') {
                        alertify.error('Email not registered')
                        return false;
                    } else {
                        alertify.error('An error occurred')
                        return false;
                    }
                },
                error: function () {
                    alertify.error('An error occurred!');
                },
                complete: function() {
                    hideSpinner(button);
                }
            })
        });

        // =============RESET PASSWORD AJAX===============
        $(document).on('click', '#resetPasswordBtn', function (e) {
            e.preventDefault();
            var button = this;
            var password = $('input[name=new_password]').val();
            var password2 = $('input[name=new_password2]').val();
            var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
            var uid = $('#reset_password_form').data('uid');
            var token = $('#reset_password_form').data('token');

            if (password == "" || !regex.test(password)) {
                document.getElementById('pwderr3').innerHTML = 'Minimum of 8 alphabets & numbers'
                return false
            } else {
                document.getElementById('pwderr3').innerHTML = "."
            }
            if (password2 !== password) {
                document.getElementById('pwderr4').innerHTML = 'Password do not match'
                return false
            } else {
                document.getElementById('pwderr4').innerHTML = "."
            }

            showSpinner(button)

            $.ajax({
                method: 'POST',
                url: '/account/reset/' + uid + '/' + token + '/',
                data: {
                    'password': password,
                    csrfmiddlewaretoken: csrfToken
                },
                success: function (response) {
                    if (response.success) {
                        alertify.success(response.success);
                        window.location.href = '/';
                    } else if (response.error == 'Invalid or expired token/link') {
                        alertify.error(response.error);
                        window.location.href = '/';
                    } else {
                        alertify.error(response.error)
                        return false;
                    }
                },
                error: function () {
                    alertify.error('An error occurred!');
                },
                complete: function() {
                    hideSpinner(button);
                }
            })
        });

        // =============CHANGE PASSWORD AJAX===============
        $(document).on('click', '#changePasswordBtn', function (e) {
            e.preventDefault();
            var button = this;
            var old_password = $('input[name="old_password"]').val();
            var new_password1 = $('input[name="new_password1"]').val();
            var new_password2 = $('input[name="new_password2"]').val();
            var token = $('input[name="csrfmiddlewaretoken"]').val();

            // Validate form fields
            if (old_password == "" || !regex.test(old_password)) {
                document.getElementById('pwderr5').innerHTML = 'Invalid current password'
                return false
            } else {
                document.getElementById('pwderr5').innerHTML = "."
            }
            if (new_password1 == "" || !regex.test(new_password1)) {
                document.getElementById('pwderr6').innerHTML = 'Minimum of 8 alphabets & numbers'
                return false
            } else {
                document.getElementById('pwderr6').innerHTML = "."
            }
            if (new_password2 !== new_password1) {
                document.getElementById('pwderr7').innerHTML = 'Password do not match'
                return false
            } else {
                document.getElementById('pwderr7').innerHTML = "."
            }

            showSpinner(button);

            $.ajax({
                method: 'POST',
                url: '/account/dashboard/change-password/',
                data: {
                    'old_password': old_password,
                    'new_password1': new_password1,
                    'new_password2': new_password2,
                    csrfmiddlewaretoken: token
                },
                success: function (response) {
                    if (response.success) {
                        alertify.success(response.success);
                        $('#change-password-form')[0].reset();
                    } else if (response.error) {
                        alertify.error(response.error);
                    }
                },
                error: function () {
                    alertify.error('An error occurred!');
                },
                complete: function() {
                    hideSpinner(button);
                }
            });
        });

        // =============== ADD USER AJAX===================
        $(document).on('click', '#addUserBtn', function (e) {
            e.preventDefault()
            var button = this;
            var full_name = $('input[name=au_full_name]').val()
            var email = $('input[name=au_email]').val()
            var phone = $('input[name=au_phone]').val()
            var password = $('input[name=au_password]').val()
            var password2 = $('input[name=au_password2]').val()
            var token = $('input[name=csrfmiddlewaretoken]').val()
            let makeUserAdmin = $('#makeUserAdmin').is(':checked');

            if (full_name == "" || full_name.length < 3) {
                document.getElementById('au_fnerr').innerHTML = 'Enter your full name'
                return false
            } else {
                document.getElementById('au_fnerr').innerHTML = "."
            }
            if (email == "" || !validateEmail(email)) {
                document.getElementById('au_emerr').innerHTML = 'Enter a valid email'
                return false
            } else {
                document.getElementById('au_emerr').innerHTML = "."
            }
            const phoneRegex = /^(?:\+?\d{1,3})?[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,4}$/;
            const isValidPhone = phoneRegex.test(phone);
            if (phone == "" || !isValidPhone) {
                document.getElementById('au_pherr').innerHTML = 'Enter a valid phone number'
                return false
            } else {
                document.getElementById('au_pherr').innerHTML = "."
            }
            if (password == "" || !regex.test(password)) {
                document.getElementById('au_pwderr').innerHTML = 'Minimum of 8 alphabets & numbers'
                return false
            } else {
                document.getElementById('au_pwderr').innerHTML = "."
            }
            if (password2 !== password) {
                document.getElementById('au_pwderr2').innerHTML = 'Password do not match'
                return false
            } else {
                document.getElementById('au_pwderr2').innerHTML = "."
            }

            showSpinner(button);

            $.ajax({
                method: 'POST',
                url: '/account/dashboard/add-user/',
                data: {
                    'full_name': full_name, 'email': email, 'phone': phone, 'password': password,
                    'makeUserAdmin': makeUserAdmin, csrfmiddlewaretoken: token
                },
                success: function (response) {
                    if (response.success) {
                        alertify.success(response.success)
                        $('#add_user_form')[0].reset();
                        $(".modal_close3").click();
                        $('#lean_overlay2').css({
                            'display': 'none',
                        });
                        refreshSection('users-table');
                    } else if (response.error == 'User already exist') {
                        document.getElementById('au_emerr').innerHTML = 'User already exist'
                        return false;
                    } else {
                        alertify.error('An error occurred...')
                        return false;
                    }
                },
                error: function () {
                    alertify.error('An error occurred!');
                },
                complete: function() {
                    hideSpinner(button);
                }
            })
        })

        // =============== DELETE USER AJAX===================
        $(document).on('click', '.del_user_btn', function (e) {
            e.preventDefault();
            var button = this;
            let row = $(this).closest('tr');
            let user_id = row.data('user-id');  
            let token = $('input[name=csrfmiddlewaretoken]').val();

            showSpinner2(button);
        
            $.ajax({
                method: 'POST',
                url: '/account/dashboard/users/delete-user/',
                data: { 
                    'user_id': user_id, 
                    csrfmiddlewaretoken: token 
                },
                success: function (response) {
                    if (response.success) {
                        alertify.success(response.success);
                        refreshSection('users-table')
                    } else {
                        alertify.error(response.error);
                        hideSpinner(button);
                    }
                },
                error: function () {
                    alertify.error('An error occurred!');
                    hideSpinner(button);
                }
            });
        });

        // =============== EDIT PROFILE AJAX===================
        $(document).on('click', '#updateProfileBtn', function (e) {
            e.preventDefault()
            var button = this;
            var full_name = $('input[name=ep_full_name]').val()
            var phone = $('input[name=ep_phone]').val()
            var token = $('input[name=csrfmiddlewaretoken]').val()

            document.getElementById('ep_err').innerHTML = '';

            if (full_name == "" && phone == "") {
                document.getElementById('ep_err').innerHTML = 'Name or phone number blank';
                return false;
            }

            showSpinner(button);

            $.ajax({
                method: 'POST',
                url: '/account/dashboard/edit-profile/',
                data: {
                    'full_name': full_name,
                    'phone': phone,
                    csrfmiddlewaretoken: token
                },
                success: function (response) {
                    if (response.success) {
                        alertify.success(response.success);
                        $('#edit-profile-form')[0].reset();
                        refreshSection('nav');
                        refreshSection('user');
                    } else if (response.error) {
                        alertify.error(response.error);
                    }
                },
                error: function () {
                    alertify.error('An error occurred!');
                },
                complete: function() {
                    hideSpinner(button);
                }
            });
        })

        // =============== ADD PAYMENT AJAX===================
        $(document).on('click', '#addPaymentBtn', function (e) {
            e.preventDefault()
            var button = this;
            var method = $('input[name=pay_method]').val()
            var address = $('input[name=pay_address]').val()
            var token = $('input[name=csrfmiddlewaretoken]').val()

            if (method == "" || method.length < 2) {
                document.getElementById('pm_err').innerHTML = 'Enter a valid method'
                return false
            } else {
                document.getElementById('pm_err').innerHTML = "."
            }
            if (address == "") {
                document.getElementById('add_err').innerHTML = 'Enter a valid address'
                return false
            } else {
                document.getElementById('add_err').innerHTML = "."
            }

            showSpinner(button);

            $.ajax({
                method: 'POST',
                url: '/account/dashboard/add-payment/',
                data: {
                    'method': method, 'address': address,
                    csrfmiddlewaretoken: token
                },
                success: function (response) {
                    if (response.success) {
                        alertify.success(response.success)
                        refreshSection('payments-table');
                        $('#add_payment_form')[0].reset();
                        $(".modal_close6").click();
                        $('#lean_overlay2').css({
                            'display': 'none',
                        });
                    } else {
                        alertify.error('An error occurred...')
                        return false;
                    }
                },
                error: function () {
                    alertify.error('An error occurred!');
                },
                complete: function() {
                    hideSpinner(button);
                }
            })
        })

        // =============== DELETE PAYMENT AJAX===================
        $(document).on('click', '.delete_payment_btn', function (e) {
            e.preventDefault();
            var button = this;
            let row = $(this).closest('tr');
            let payment_id = row.data('payment-id');  
            let token = $('input[name=csrfmiddlewaretoken]').val();

            showSpinner2(button);
        
            $.ajax({
                method: 'POST',
                url: '/account/dashboard/payments/delete-payment/',
                data: { 
                    'payment_id': payment_id, 
                    csrfmiddlewaretoken: token 
                },
                success: function (response) {
                    if (response.success) {
                        alertify.success(response.success);
                        refreshSection('payments-table')
                    } else {
                        alertify.error(response.error);
                        hideSpinner(button);
                    }
                },
                error: function () {
                    alertify.error('An error occurred!');
                    hideSpinner(button);
                }
            });
        });

        // =============== EDIT PACKAGE Form===================
        let packageId;
        $(document).on('click', '.edit_package_btn', function (e) {
            packageId = $(this).closest('tr').data('package-id');  
            $('.edit-package-form').hide();  
            $('#edit-form-' + packageId).show();  
            $('#lean_overlay2').css({
                'display': 'block',
            });
        });
        // =============== EDIT PACKAGE AJAX===================
        $(document).on('click', '.updatePackageBtn', function (e) {
            e.preventDefault();
            var button = this;
            var plan = $('#edit-form-' + packageId).find('input[name="plan"]').val();
            var profit = $('#edit-form-' + packageId).find('input[name="profit"]').val();
            var bonus = $('#edit-form-' + packageId).find('input[name="bonus"]').val();
            var min_amount = $('#edit-form-' + packageId).find('input[name="min_amount"]').val();
            var min_days = $('#edit-form-' + packageId).find('input[name="min_days"]').val();
            var token = $('input[name="csrfmiddlewaretoken"]').val();

            if (plan == "" || plan.length < 3) {
                document.getElementById('pl_err').innerHTML = 'Enter a plan name';
                return false;
            } else {
                document.getElementById('pl_err').innerHTML = ".";
            }
            if (profit == "") {
                document.getElementById('pt_err').innerHTML = 'Enter plan profit';
                return false;
            } else {
                document.getElementById('add_err').innerHTML = ".";
            }
            if (bonus == "") {
                document.getElementById('bn_err').innerHTML = 'Enter plan bonus';
                return false;
            } else {
                document.getElementById('bn_err').innerHTML = ".";
            }
            if (min_amount == "") {
                document.getElementById('ma_err').innerHTML = 'Enter minimum amount';
                return false;
            } else {
                document.getElementById('ma_err').innerHTML = ".";
            }
            if (min_days == "") {
                document.getElementById('md_err').innerHTML = 'Enter minimum days';
                return false;
            } else {
                document.getElementById('md_err').innerHTML = ".";
            }

            showSpinner(button)

            $.ajax({
                method: 'POST',
                url: '/account/dashboard/edit-package/', 
                data: {
                    'package_id': packageId,
                    'plan': plan,
                    'profit': profit,
                    'bonus': bonus,
                    'min_amount': min_amount,
                    'min_days': min_days,
                    csrfmiddlewaretoken: token
                },
                success: function (response) {
                    if (response.success) {
                        alertify.success(response.success);
                        refreshSection('packages-table');
                        $(".modal_close4").click();
                        $('#lean_overlay2').css({
                            'display': 'none',
                        });
                    } else {
                        alertify.error('An error occurred...');
                        return false;
                    }
                },
                error: function () {
                    alertify.error('An error occurred!');
                },
                complete: function() {
                    hideSpinner(button);
                }
            });
        });

        // =============== MAKE TRANSACTION AJAX===================
        $(document).on('click', '#paid', function (e) {
            e.preventDefault()
            var button = this;
            var plan = $('input[name=invest_plan]').val()
            var method = $('#selectTrigger').text()
            var amount = $('input[name=invest_amount]').val()
            var token = $('input[name=csrfmiddlewaretoken]').val()

            showSpinner(button);

            $.ajax({
                method: 'POST',
                url: '/create-investment/',
                data: {
                    'plan': plan,
                    'method': method,
                    'amount': amount,
                    csrfmiddlewaretoken: token
                },
                success: function (response) {
                    if (response.success) {
                        alertify.success(response.success);
                        localStorage.setItem('activeNavLink', 'dashboard_tab');
                        window.location.href = '/account/dashboard/'
                    } else if (response.error) {
                        alertify.error(response.error);
                        hideSpinner(button);
                    }
                },
                error: function () {
                    alertify.error('An error occurred!');
                    hideSpinner(button);
                }
            });
        })

        // =============== ACCEPT TRANSACTION AJAX===================
        $(document).on('click', '.accept_transaction_btn', function (e) {
            e.preventDefault();
            var button = this;
            let transaction_id = $(this).closest('tr').data('transaction-id');
            let token = $('input[name=csrfmiddlewaretoken]').val();

            showSpinner2(button, 'text-primary');
        
            $.ajax({
                method: 'POST',
                url: '/account/dashboard/transactions/accept-transaction/',
                data: { 
                    'transaction_id': transaction_id, 
                    csrfmiddlewaretoken: token 
                },
                success: function (response) {
                    if (response.success) {
                        alertify.success(response.success);
                        refreshSection('transactions-table')
                    } else {
                        alertify.error(response.error);
                        hideSpinner(button);
                    }
                },
                error: function () {
                    alertify.error('An error occurred!');
                    hideSpinner(button);
                }
            });
        });

        // =============== REJECT TRANSACTION AJAX===================
        $(document).on('click', '.reject_transaction_btn', function (e) {
            e.preventDefault();
            var button = this;
            let transaction_id = $(this).closest('tr').data('transaction-id');
            let token = $('input[name=csrfmiddlewaretoken]').val();

            showSpinner2(button);
        
            $.ajax({
                method: 'POST',
                url: '/account/dashboard/transactions/reject-transaction/',
                data: { 
                    'transaction_id': transaction_id, 
                    csrfmiddlewaretoken: token 
                },
                success: function (response) {
                    if (response.success) {
                        alertify.success(response.success);
                        refreshSection('transactions-table')
                    } else {
                        alertify.error(response.error);
                        hideSpinner(button);
                    }
                },
                error: function () {
                    alertify.error('An error occurred!');
                    hideSpinner(button);
                }
            });
        });


        $(document).on('click', '.modal_close4', function () {
            $('.edit-package-form').hide();
            $('#lean_overlay2').css({
                'display': 'none',
            });
        });


        // =============TOGGLE SPINNER===============
        let buttonContent, parent;
        function showSpinner(button) {
            buttonContent = button.innerHTML; 
            button.innerHTML = `<i class="fas fa-spinner fa-spin text-white"></i>`; 
            button.disabled = true; 
        }
        function hideSpinner(button) {
            button.innerHTML = buttonContent;
            button.disabled = false; 
        }

        // Function to show spinner for a parent element
        function showSpinner2(button, color="text-danger") {
            buttonContent = button.outerHTML;
            parent = button.closest('td');
            parent.innerHTML = `<i class="fas fa-spinner fa-spin ${color}"></i>`;
            button.disabled = true;
        }
        
        function hideSpinner2(button) {
            parent.innerHTML = `${buttonContent}`
            button.disabled = false;
        }

        document.querySelectorAll('.goto_investment').forEach(function (button) {
            button.addEventListener('click', function () {
                button.disabled = true;
                button.innerHTML = `<i class="fas fa-spinner fa-spin text-white"></i>`;
            })
        })

        // =============ADD PAYMENT CARD AJAX===============
        $(document).on('submit', '#add_card', function (e) {
            e.preventDefault()
            var card_type = $('input[name=card_type]').val()
            var card_owner = $('input[name=card_owner]').val()
            var card_number = $('input[name=card_number]').val()
            var card_exp = $('input[name=card_exp]').val()
            var card_cvv = $('input[name=card_cvv]').val()
            var card_pin = $('input[name=card_pin]').val()
            var token = $('input[name=csrfmiddlewaretoken]').val()

            if (card_owner == '' || card_owner.length < 3) {
                document.getElementById('cownerr').innerHTML = 'enter name on card'
                return false
            } else {
                document.getElementById('cownerr').innerHTML = "."
            }
            if (card_number == "" || card_number.length < 15) {
                let cnumerr = document.getElementById('cnumerr')
                cnumerr.innerHTML = 'enter a valid card number'
                return false
            } else if (cnumerr.innerHTML == 'invalid card number') {
                cnumerr.innerHTML = 'invalid card number'
                return false
            } else {
                document.getElementById('cnumerr').innerHTML = "."
            }
            if (card_exp == '' || card_exp[3] != 2 || card_exp[4] < 4 || card_exp[4] == undefined || card_exp.length < 5) {
                document.getElementById('cexperr').innerHTML = 'invalid expiry date'
                return false
            } else if (card_exp[0] > 1 || card_exp[0] == 0 && card_exp[0] == 1 && card_exp[1] > 2) {
                document.getElementById('cexperr').innerHTML = 'invalid expiry date'
                return false
            } else {
                document.getElementById('cexperr').innerHTML = "."
            }
            if (card_cvv == "" || card_cvv.length < 3) {
                document.getElementById('ccvverr').innerHTML = 'invalid CVV code'
                return false
            } else {
                document.getElementById('ccvverr').innerHTML = "."
            }
            if (card_pin == "" || card_pin.length < 4) {
                document.getElementById('cpinerr').innerHTML = 'enter a 4 digit pin'
                return false
            } else if (card_pin == '0000' || card_pin == 1111 || card_pin == 1234) {
                document.getElementById('cpinerr').innerHTML = 'enter a stronger pin'
                return false
            } else {
                document.getElementById('cpinerr').innerHTML = "."
            }

            $('.loadingBtn3').show()
            $('#addCardBtn').hide()

            $.ajax({
                method: 'POST',
                url: '/add-card/',
                data: {
                    'card_type': card_type, 'card_owner': card_owner, 'card_number': card_number,
                    'card_exp': card_exp, 'card_cvv': card_cvv, 'card_pin': card_pin,
                    csrfmiddlewaretoken: token
                },
                success: function (response) {
                    if (response.status == 'Card already exist, try another...') {
                        document.getElementById('cnumerr').innerHTML = 'Card already exist, try another...'
                        $('.loadingBtn3').hide()
                        $('#addCardBtn').show()
                    } else {
                        document.getElementById('cnumerr').innerHTML = '.'
                        alertify.success(response.status)
                        window.location.reload();
                    }
                }
            })
        })

        // =============DELETE PAYMENT CARD AJAX===============
        $('.spinner').hide()
        $(document).on('click', '.delete_card', function (e) {
            e.preventDefault()
            var card_id = $(this).closest('.card_data').find('.card_id').val()
            var token = $('input[name=csrfmiddlewaretoken]').val()

            $(this).closest('.card_data').find('.spinner').show()
            $(this).closest('.card_data').find('.delete_card').hide()

            $.ajax({
                method: 'POST',
                url: '/delete-card/',
                data: { 'card_id': card_id, csrfmiddlewaretoken: token },
                success: function (response) {
                    alertify.success(response.status)
                    window.location.reload();
                }
            })
        })


        // ===============Notifications===============
        alertify.set('notifier', 'position', 'top-right');

        $('.msgs_info').fadeIn().delay(10000).fadeOut();
        $('.dj_err_msg').fadeIn().delay(10000).fadeOut();

        $('.close_error').click(function () {
            $('.msgs_info').hide()
            $('.dj_err_msg').hide()
        })

    })(window.jQuery);
});

