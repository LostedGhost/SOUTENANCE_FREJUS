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
app = Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            email: '',
            password: '',
        }
    },
    methods: {
        login() {
            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            axios.defaults.headers.common['X-CSRFToken'] = csrfToken;
            axios.get('/api/login?email='+this.email+'&password='+this.password)
            .then(response => {
                if (response.data.status == 200){
                    window.location.href = '/dash';
                }
                else{
                    showError(response.data.message);
                }
            })
        }
    },
})
if (document.getElementById("login")){
    app.mount("#login")
}
