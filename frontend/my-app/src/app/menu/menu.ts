import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../api.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-menu',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <h2>Send Data</h2>
    <textarea [(ngModel)]="payload" rows="5" cols="30"></textarea>
    <br>
    <button (click)="send()">Send</button>
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

    this.api.sendRequest(data).subscribe({
      next: res => {
        this.response = res; // store response to display
        console.log(res);
      },
      error: err => console.error('HTTP Error:', err)
    });
  }
}
