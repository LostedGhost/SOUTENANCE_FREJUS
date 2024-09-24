function drawAnswer(risque) {
    (function (factory) {
      typeof define === 'function' && define.amd ? define(factory) :
      factory();
    })(function () { 
      'use strict';
      const gaugeGradeChartInit = () => {
        const { getColor, getData } = window.phoenix.utils;
        const a = document.querySelector("#answerPredict");
        a.innerHTML = "";
        
        if (a) {
          const o = getData(a, "echarts");
          const r = window.echarts.init(a);
          
          // Configure et dessine le graphique
          r.setOption({
            series: [{
              radius: "100%",
              type: "gauge",
              center: ["50%", "70%"],
              startAngle: 180,
              endAngle: 0,
              min: 0,
              max: 1,
              splitNumber: 10,
              axisLine: {
                lineStyle: {
                  width: 6,
                  color: [
                    [.33, getColor("success")],
                    [.66, getColor("warning")],
                    [1, getColor("danger")]
                  ]
                }
              },
              pointer: {
                icon: "path://M12.8,0.7l12,40.1H0.7L12.8,0.7z",
                length: "12%",
                width: 20,
                offsetCenter: [0, "-60%"],
                itemStyle: { color: "auto" }
              },
              axisTick: {
                length: 12,
                lineStyle: { color: "auto", width: 2 }
              },
              splitLine: {
                length: 20,
                lineStyle: { color: "auto", width: 5 }
              },
              axisLabel: {
                color: getColor("quaternary-color"),
                distance: -60
              },
              title: {
                offsetCenter: [0, "-20%"],
                color: getColor("tertiary-color")
              },
              detail: {
                offsetCenter: [0, "0%"],
                valueAnimation: true,
                formatter: e => Math.round(e * 100),
                color: "auto"
              },
              data: [{ value: risque, name: "Risque" }]
            }]
          });
        }
      };
  
      // Exécuter immédiatement pour dessiner le graphe
      gaugeGradeChartInit();
    });
  }
  
app = Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            age: "",
            poids: "",
            taille: "",
            glycemie: "",
            sexe: 1,
            enceinte: 0,
            is_predict: false,
            message: "",
            answer: "",
        }
    },
    methods: {
        predict_diabete(){
            axios.get("/predict_diabete_api?age="+this.age+"&poids="+this.poids+"&taille="+this.taille+"&glycemie="+this.glycemie+"&etat_de_grossesse="+this.enceinte )
            .then(response => {
                if (response.data.status==200){
                    this.is_predict = true;
                    this.answer = response.data.answer;
                    this.message = response.data.message;
                    drawAnswer(response.data.decimal_answer);
                }
            })
        },
    },
})
if (document.getElementById("predict")){
    app.mount("#predict")
}