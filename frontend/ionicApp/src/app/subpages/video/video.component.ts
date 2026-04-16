import { Component, OnInit } from '@angular/core';
import { SafePipe } from '../../pipes/safe-pipe';
import { IonicModule } from '@ionic/angular';


@Component({
  selector: 'app-video',
  templateUrl: './video.component.html',
  styleUrls: ['./video.component.scss'],
  imports: [SafePipe,IonicModule]
})
export class VideoComponent  implements OnInit {
  videoUrl: string = "https://www.youtube.com/embed/E4ePZqypTfY";
  constructor() { }

  ngOnInit() {}

}
