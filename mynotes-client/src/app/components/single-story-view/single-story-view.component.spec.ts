import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SingleStoryViewComponent } from './single-story-view.component';

describe('SingleStoryViewComponent', () => {
  let component: SingleStoryViewComponent;
  let fixture: ComponentFixture<SingleStoryViewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SingleStoryViewComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SingleStoryViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
