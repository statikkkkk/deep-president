import { PolispeechAngularPage } from './app.po';

describe('polispeech-angular App', function() {
  let page: PolispeechAngularPage;

  beforeEach(() => {
    page = new PolispeechAngularPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
