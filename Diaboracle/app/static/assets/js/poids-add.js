
  
app = Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            poids: 0,
        }
    },
    methods: {
        enregistrer(){
            
        }
    },
})
if (document.getElementById("poids-add")){
    app.mount("#poids-add")
}