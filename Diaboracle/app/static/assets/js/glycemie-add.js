
  
app = Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            glycemie: 0,
        }
    },
    methods: {
        enregistrer(){
            
        }
    },
})
if (document.getElementById("glycemie-add")){
    app.mount("#glycemie-add")
}