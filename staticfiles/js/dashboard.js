document.addEventListener('DOMContentLoaded', function() {
    const dashNavs = document.querySelectorAll('.dash-navs');
    const dashTabs = document.querySelectorAll('.dash-tabs');

    function setActiveSection(targetId) {
        dashTabs.forEach(dashTab => dashTab.classList.remove('active'));
        dashNavs.forEach(dashNav => dashNav.classList.remove('active'));

        const targetElement = document.getElementById(targetId);
        if (targetElement) {
            targetElement.classList.add('active');
        }

        const tableContainer = targetElement.querySelector('.table-container'); 
        if (tableContainer) {
            const classList = Array.from(tableContainer.classList);
            const dynamicClass = classList.filter(cls => cls !== 'table-container')[0];
            if (dynamicClass) {
                localStorage.setItem('active-table', dynamicClass);
            }
        }

        const activeLink = document.querySelector(`#goto_${targetId}`);
        if (activeLink) {
            activeLink.classList.add('active');
        }

        const activeTable = localStorage.getItem('active-table');
        if (activeTable) {
            refreshSection(activeTable);
        }
        if (targetId == 'dashboard_tab'){
            refreshSection('dash-cards');
            refreshSection('dash-users-table');
            refreshSection('dash-transactions-table');
        }
    }

    dashNavs.forEach(dashNav => {
        dashNav.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.id.replace('goto_', '');
            setActiveSection(targetId);
            localStorage.setItem('activeNavLink', targetId);
            $('#sidebar_trigger').show();
            $('#sidebar_trigger2').removeClass('active');
            $('.sidebar').removeClass('active');
        });
    });

    const savedLink = localStorage.getItem('activeNavLink');
    if (savedLink) {
        setActiveSection(savedLink);
    } else {
        setActiveSection('dashboard_tab');
    }

    function refreshSection(element) {
        let selector = element.startsWith('#') ? element : '.' + element;

        $(selector).load(location.href + ' ' + selector + ' > *', function() {
            $('#lean_overlay2').css({'display': 'none'});
            console.log('Refreshed ' + element);
        });
    }

    setInterval(function() {
        refreshSection('dash-cards');
    }, 60000);

    $(document).on('click', '.custom-select-trigger2', function () {
        $('.custom-options').toggleClass('d-block');
    });

    $(document).on('click', '.custom-option', function () {
        let wallet = $(this).data('wallet');
        let upd = $(`<input class="login__input child" name="withdraw_wallet" value="${wallet}" style="width:80%;" readonly/>`);
        $('.child').attr('name', '');
        $('.child').attr('value', '');
        $('.child').addClass('d-none');
        $('.selDiv').prepend(upd);
    
        $('.custom-options').removeClass('d-block'); 
    });

    $(document).on('click', function(e) {
        if (!$(e.target).closest('.custom-select').length) {
            $('.custom-options').removeClass('d-block');
        }
    });


    // CHART FUNCTIONALITY
    let combinedChart;
    let userChart;

    function showSpinner() {
        document.getElementById('chartSpinner').style.display = 'block';
    }

    function hideSpinner() {
        document.getElementById('chartSpinner').style.display = 'none';
    }

    // Function to fetch data from the Django backend
    function fetchChartData() {
        showSpinner();
        $.ajax({
            url: '/account/api/fuckof/@/fuckof/get-chart-data/', 
            type: 'GET',
            dataType: 'json',
            success: function (response) {
                updateChart(response);
                hideSpinner();
            },
            error: function (xhr, status, error) {
                // console.error('Error fetching chart data:', error);
            }
        });
    }

    function fetchUserChartData() {
        showSpinner();
        $.ajax({
            url: '/account/api/fuckof/@/fuckof/get-user-chart-data/', 
            type: 'GET',
            dataType: 'json',
            success: function (response) {
                updateUserChart(response);
                hideSpinner();
            },
            error: function (xhr, status, error) {
                // console.error('Error fetching chart data:', error);
            }
        });
    }

    // Function to update the chart with the fetched data
    function updateChart(data) {
        const labels = data.labels;
        const usersData = data.users;
        const investmentsData = data.investments;
        const roiData = data.roi;

        console.log('Users Data:', usersData); // Add console log to verify users data
        console.log('Investments Data:', investmentsData); // Add console log to verify investments data
        console.log('ROI Data:', roiData); // Add console log to verify ROI data

        // Update Combined Chart
        if (combinedChart) {
            combinedChart.data.labels = labels;
            combinedChart.data.datasets[0].data = usersData;
            combinedChart.data.datasets[1].data = investmentsData;
            combinedChart.data.datasets[2].data = roiData;
            combinedChart.update();
        } else {
            const ctxCombined = document.getElementById('combinedChart').getContext('2d');
            combinedChart = new Chart(ctxCombined, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Total Users',
                            data: usersData,
                            borderColor: '#4a8ef3',
                            backgroundColor: 'rgba(74, 142, 243, 0.2)',
                            borderWidth: 2,
                            fill: true
                        },
                        {
                            label: 'Total Investments',
                            data: investmentsData,
                            borderColor: '#4caf50',
                            backgroundColor: 'rgba(76, 175, 80, 0.2)',
                            borderWidth: 2,
                            fill: true
                        },
                        {
                            label: 'Total ROI',
                            data: roiData,
                            borderColor: '#ff9800',
                            backgroundColor: 'rgba(255, 152, 0, 0.2)',
                            borderWidth: 2,
                            fill: true
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            labels: {
                                color: '#000'
                            }
                        }
                    },
                    scales: {
                        x: {
                            ticks: {
                                color: '#000'
                            },
                            grid: {
                                color: '#ccc'
                            }
                        },
                        y: {
                            ticks: {
                                color: '#000'
                            },
                            grid: {
                                color: '#ccc'
                            },
                            beginAtZero: true
                        }
                    }
                }
            });
        }
    }

    function updateUserChart(data) {
        const labels = data.labels;
        const investmentsData = data.investments;
        const roiData = data.roi;

        console.log('User Investments Data:', investmentsData); // Add console log to verify investments data
        console.log('User ROI Data:', roiData); // Add console log to verify ROI data

        // Update User Chart
        if (userChart) {
            userChart.data.labels = labels;
            userChart.data.datasets[0].data = investmentsData;
            userChart.data.datasets[1].data = roiData;
            userChart.update();
        } else {
            const ctxUser = document.getElementById('userChart').getContext('2d');
            userChart = new Chart(ctxUser, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'User Investments',
                            data: investmentsData,
                            borderColor: '#4caf50',
                            backgroundColor: 'rgba(76, 175, 80, 0.2)',
                            borderWidth: 2,
                            fill: true
                        },
                        {
                            label: 'User ROI',
                            data: roiData,
                            borderColor: '#ff9800',
                            backgroundColor: 'rgba(255, 152, 0, 0.2)',
                            borderWidth: 2,
                            fill: true
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            labels: {
                                color: '#000'
                            }
                        }
                    },
                    scales: {
                        x: {
                            ticks: {
                                color: '#000'
                            },
                            grid: {
                                color: '#ccc'
                            }
                        },
                        y: {
                            ticks: {
                                color: '#000'
                            },
                            grid: {
                                color: '#ccc'
                            },
                            beginAtZero: true
                        }
                    }
                }
            });
        }
    }


    // Function to get CSRF token
    function getCSRFToken() {
        let csrfToken = null;
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith('csrftoken=')) {
                csrfToken = cookie.substring('csrftoken='.length, cookie.length);
                break;
            }
        }
        return csrfToken;
    }

    // Function to update ROI every 30 seconds
    function updateROIdaily() {
        const csrfToken = getCSRFToken();
        $.ajax({
            url: '/account/api/update-roi/', 
            type: 'POST',
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrfToken
            },
            success: function (response) {
                console.log('ROI update response:', response);
            },
            error: function (xhr, status, error) {
                console.error('Error updating ROI:', error);
            }
        });
    }    


    fetchChartData();
    fetchUserChartData();
    setInterval(fetchChartData, 60000);
    setInterval(fetchUserChartData, 60000);
    setInterval(updateROIdaily, 60000);
});

