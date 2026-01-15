import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../api.service';

@Component({
  selector: 'app-menu',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <h2>Dashboard</h2>
    <textarea [(ngModel)]="payload" rows="5" cols="30" placeholder="Enter JSON"></textarea>
    <br/>
    <button (click)="send()">Send Request</button>
    <pre>{{ response | json }}</pre>
  `
})
export class MenuComponent {
  payload = '';
  response: any;

  constructor(private api: ApiService) {}

  send() {
    let data;
    try {
      data = JSON.parse(this.payload);
    } catch {
      alert('Invalid JSON');
      return;
    }
    console.log("test");

  
    
  }
}
