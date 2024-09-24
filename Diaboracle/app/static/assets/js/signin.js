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
            nom: '',
            prenoms: '',
            date_naissance: '',
            email: '',
            password: '',
            repassword: '',
            is_specialiste: false,
            speciality: '',
        }
    },
    methods: {
        signin() {
            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            axios.defaults.headers.common['X-CSRFToken'] = csrfToken;
            axios.get('/api/signin?nom='+this.nom+'&prenoms='+this.prenoms+'&date_naissance='+this.date_naissance+'&email='+this.email+'&password='+this.password+'&repassword='+this.repassword+'&speciality='+this.speciality)
            .then(response => {
                if (response.data.status == 200){
                    window.location.href = '/login';
                }
                else{
                    showError(response.data.message);
                }
            })
        }
    },
})
if (document.getElementById("signin")){
    app.mount("#signin")
}
