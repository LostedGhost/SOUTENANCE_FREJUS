function showError(error) {
    Swal.fire({
        icon: "error",
        title: "Erreur",
        text: error,
        error: null
    });
}

function showSuccess(success) {
    Swal.fire({
        icon: "success",
        title: "Succès",
        text: success,
        error: null
    });
}

function createLineChart(chartId, constante, labels, data) {
    // Récupère le contexte du canvas où le graphique sera rendu
    if (chartInstance) {
        chartInstance.destroy();
    }
    const ctx = document.getElementById(chartId).getContext('2d');

    // Crée le graphique
    chartInstance = new Chart(ctx, {
        type: 'line',  // Type de graphique: line chart
        data: {
            labels: labels,  // Valeurs pour l'axe des x
            datasets: [{
                label: constante,
                data: data,  // Valeurs pour l'axe des y
                borderColor: 'rgba(75, 192, 192, 1)',  // Couleur de la ligne
                borderWidth: 2,
                fill: false  // Pas de remplissage sous la ligne
            }]
        },
        options: {
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Temps'
                    }
                },
                y: {
                    beginAtZero: true,  // L'axe des y commence à zéro
                    title: {
                        display: true,
                        text: 'Valeur'
                    }
                }
            },
            responsive: true
        }
    });
}



app = Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            constante: 'Poids',
            valeur: '',
            option: 0,
            start: '',
            end: '',
            mois: '',
        }
    },
    methods: {
        createLineChart(){
            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            axios.defaults.headers.common['X-CSRFToken'] = csrfToken;
            const path = window.location.pathname;
            // Divise le chemin par les "/"
            const parts = path.split("/");

            // Récupère le dernier élément du tableau
            const lastPart = parts.pop() || parts.pop();
            axios.get('/api/getGrapheDatasPatient/'+lastPart+'?option='+this.option+'&constante='+this.constante+'&mois='+this.mois+'&start='+this.start+'&end='+this.end)
            .then(response => {
                if (response.data.status == 200){
                    createLineChart('graphe', this.constante, response.data.period, response.data.datas);
                }
                else{
                    showError(response.data.message);
                }
            })
        },
        getDatas(){
            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            axios.defaults.headers.common['X-CSRFToken'] = csrfToken;
            axios.get('/api/getDatas?option='+this.option+'&constante='+this.constante+'&mois='+this.mois+'&start='+this.start+'&end='+this.end)
            .then(response => {
                if (response.data.status == 200){
                    this.valeur = response.data.valeur;
                }
                else{
                    showError(response.data.message);
                }
            })
        },
        validateMonth(){
            this.createLineChart();
            document.getElementById("dismissMonthModal").click();
        },
        setMinEnd(){
            document.getElementById("end").setAttribute('min', this.start);
            document.getElementById("end").value = this.start;
        },
        validatePeriod(){
            this.createLineChart();
            document.getElementById("dismissPeriodModal").click();
        }
    },
    mounted() {
        // Exemple d'utilisation avec des valeurs fictives
        //createLineChart('graphe', 'Poids', ['Janvier', 'Février', 'Mars', 'Avril'], [65, 59, 80, 81]);
        this.createLineChart();
    },
})
if (document.getElementById("dash_patient")){
    app.mount("#dash_patient")
}
