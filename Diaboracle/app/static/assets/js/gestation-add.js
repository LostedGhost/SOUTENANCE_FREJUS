
  
app = Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            enceinte: 0,
        }
    },
    methods: {
        enregistrer(){
            
        }
    },
})
if (document.getElementById("gestation-add")){
    app.mount("#gestation-add")
}