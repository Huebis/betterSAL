import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Fileviewer } from './fileviewer';

describe('Fileviewer', () => {
  let component: Fileviewer;
  let fixture: ComponentFixture<Fileviewer>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Fileviewer]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Fileviewer);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
