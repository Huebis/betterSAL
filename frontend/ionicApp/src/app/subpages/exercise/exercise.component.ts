import { Component, OnInit } from '@angular/core';

export interface Solution

export interface exercise{
  solution:Array<string,number>
  sentence:string
  help:string

}


@Component({
  selector: 'app-exercise',
  templateUrl: './exercise.component.html',
  styleUrls: ['./exercise.component.scss'],
})
export class ExerciseComponent  implements OnInit {



  constructor() { }

  ngOnInit() {}

}
