import { Component, OnInit } from '@angular/core';
import { IonInput } from "@ionic/angular/standalone";
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
}


@Component({
  selector: 'app-exercise',
  templateUrl: './exercise.component.html',
  styleUrls: ['./exercise.component.scss'],
  imports: [IonInput,FormsModule],
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
  }
  ]
  position:number=0;

  constructor() { }

  ngOnInit() {}

}
