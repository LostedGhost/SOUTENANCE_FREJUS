function drawAnswer(answer, message){
    (function (factory) {
        typeof define === 'function' && define.amd ? define(factory) :
        factory();
      })((function () { 'use strict';
    const gaugeGradeChartInit=()=>{const{getColor:e,getData:t}=window.phoenix.utils,a=document.querySelector(".answerPredict");if(a){const o=t(a,"echarts"),r=window.echarts.init(a);echartSetOption(r,o,(()=>({series:[{radius:"100%",type:"gauge",center:["50%","70%"],startAngle:180,endAngle:0,min:0,max:1,splitNumber:8,axisLine:{lineStyle:{width:6,color:[[.25,e("danger")],[.5,e("warning")],[.75,e("info")],[1,e("success")]]}},pointer:{icon:"path://M12.8,0.7l12,40.1H0.7L12.8,0.7z",length:"12%",width:20,offsetCenter:[0,"-60%"],itemStyle:{color:"auto"}},axisTick:{length:12,lineStyle:{color:"auto",width:2}},splitLine:{length:20,lineStyle:{color:"auto",width:5}},axisLabel:{color:e("quaternary-color"),distance:-60,formatter:e=>.875===e?"Excellent":.625===e?"Good":.375===e?"Well":.125===e?"Bad":""},title:{offsetCenter:[0,"-20%"],color:e("tertiary-color")},detail:{offsetCenter:[0,"0%"],valueAnimation:!0,formatter:e=>Math.round(100*e),color:"auto"},data:[{value:answer,name:"Risque"}]}]})));}};
    const{docReady:docReady}=window.phoenix.utils;
    docReady(gaugeGradeChartInit);
}));
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