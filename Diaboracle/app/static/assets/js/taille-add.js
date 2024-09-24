
  
app = Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            taille: 0,
        }
    },
    methods: {
        enregistrer(){
            
        }
    },
})
if (document.getElementById("taille-add")){
    app.mount("#taille-add")
}