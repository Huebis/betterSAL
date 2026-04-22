import { Component, OnInit } from '@angular/core';
import { IonInput, IonButton } from "@ionic/angular/standalone";
import { FormsModule } from '@angular/forms';

export interface Exercise{
  input:Array<{ 
    text:string
    solution:string
    position:number
    lastPosition:number
  }>
  sentence:string
  help:string
  instruction:string
}


@Component({
  selector: 'app-exercise',
  templateUrl: './exercise.component.html',
  styleUrls: ['./exercise.component.scss'],
  imports: [IonInput, FormsModule, IonButton],
})
export class ExerciseComponent  implements OnInit {
  exercises:Array<Exercise>=[{
    input:[{
      text:"",
      solution:"blabla",
      position:9,
      lastPosition:0,
    }],
    sentence:"1234567890123456789",
    help:"",
    instruction:"fill in the blank",
  }
  ]
  position:number=0;
  status:boolean=false;

  constructor() { }

  ngOnInit() {
    let input=localStorage.getItem("english")
    if (input!=null){
      let Object=JSON.parse(input);
      for (let i=0; i<Object.length; i++){
        for (let a=0; a<Object[i].length; a++){
          this.exercises[i].input[a].text = Object[i][a];
        }
      }
        
    }
  }
  check(){
    console.log("test");
    this.status=true;
    localStorage.setItem("english", JSON.stringify(this.exercises.map( exercise => {return exercise.input.map(input => input.text)})))
    console.log("test");
  }
  next(){}


}
