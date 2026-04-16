import { Component, OnInit } from '@angular/core';
import { SafePipe } from '../../pipes/safe-pipe';

@Component({
  selector: 'app-video',
  templateUrl: './video.component.html',
  styleUrls: ['./video.component.scss'],
})
export class VideoComponent  implements OnInit {
  videoUrl: string = "https://www.youtube.com/watch?v=E4ePZqypTfY";
  constructor() { }

  ngOnInit() {}

}
