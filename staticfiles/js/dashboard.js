document.addEventListener('DOMContentLoaded', function() {
    let userData, investmentData, roiData, usersChart, investmentChart, roiChart;

    // Initialize data (can be fetched from Django backend)
    const labels = ['2025'];  // Single label for the year

    function initialData() {
        // Example initial data, can be updated dynamically from backend
        userData = [0];  // Initial number of users (starting at 0)
        investmentData = [0];  // Initial investment value (starting at 0)
        roiData = [0];  // Initial ROI value (starting at 0)
    }

    function createCharts() {
        // Create the Users chart
        const ctxUsers = document.getElementById('usersChart').getContext('2d');
        usersChart = new Chart(ctxUsers, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Total Users',
                    data: userData,
                    color: '#fff',
                    borderColor: '#fff',
                    backgroundColor: '#4a8ef3',
                    borderWidth: 2,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: '#fff'
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            color: '#fff'
                        },
                        grid: {
                            color: '#fff'
                        }
                    },
                    y: {
                        ticks: {
                            color: '#fff'
                        },
                        grid: {
                            color: '#fff'
                        },
                        beginAtZero: true
                    }
                }
            }
        });

        // Create the Investment chart
        const ctxInvestment = document.getElementById('investmentChart').getContext('2d');
        investmentChart = new Chart(ctxInvestment, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Total Investments',
                    data: investmentData,
                    color: '#fff',
                    borderColor: '#fff',
                    backgroundColor: '#4a8ef3',
                    borderWidth: 2,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: '#fff'
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            color: '#fff'
                        },
                        grid: {
                            color: '#fff'
                        }
                    },
                    y: {
                        ticks: {
                            color: '#fff'
                        },
                        grid: {
                            color: '#fff'
                        },
                        beginAtZero: true
                    }
                }
            }
        });

        // Create the ROI chart
        const ctxROI = document.getElementById('roiChart').getContext('2d');
        roiChart = new Chart(ctxROI, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Total ROI',
                    data: roiData,
                    color: '#fff',
                    borderColor: '#fff',
                    backgroundColor: '#4a8ef3',
                    borderWidth: 2,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: '#fff'
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            color: '#fff'
                        },
                        grid: {
                            color: '#fff'
                        }
                    },
                    y: {
                        ticks: {
                            color: '#fff'
                        },
                        grid: {
                            color: '#fff'
                        },
                        beginAtZero: true
                    }
                }
            }
        });
    }

    initialData();
    createCharts();

    // Function to update chart data dynamically
    function updateChartData(type, value) {
        if (type === 'user') {
            userData.push(userData[userData.length - 1] + 1);  // Add 1 for new user
            usersChart.update();
        }
        else if (type === 'investment') {
            investmentData.push(investmentData[investmentData.length - 1] + value);  // Add invested amount
            investmentChart.update();
        }
        else if (type === 'roi') {
            roiData.push(roiData[roiData.length - 1] + value);  // Add ROI amount
            roiChart.update();
        }
    }

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
    }

    dashNavs.forEach(dashNav => {
        dashNav.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.id.replace('goto_', '');
            setActiveSection(targetId);
            localStorage.setItem('activeNavLink', targetId);
            getActive();
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

    function getActive() {
        let activeTable = localStorage.getItem('active-table');
        if (activeTable) {
            refreshSection(activeTable);
        }
    }
    
    function refreshSection(element) {
        let selector = element.startsWith('#') ? element : '.' + element;
        $(selector).load(location.href + ' ' + selector + ' > *', function() {
            $('#lean_overlay2').css({
                'display': 'none',
            });
            console.log('Refreshed ' + element);
        });
    }
    
    // setInterval(function() {
    //     getActive();
    // }, 10000);


    //wallet details dropdown
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
});
// function FetchDashboardData() {
//     $.ajax({
//         method: 'GET',
//         url: '/account/fuckoff@75109090@fuckoff/',
//         success: function(data) {
//             $('dashboard').html(JSON.stringify(data));
//             console.log('Fetch successful');
//             console.log(data);
//         },
//         error: function(xhr, status, error) {
//             console.error('Error:', error);
//         }
//     });
// }




