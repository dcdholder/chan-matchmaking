class Chart extends React.Component {
  constructor (props) { //TODO: change this to a yaml parser when you're done testing out the basic UI
    super(props);

    this.tagLine = "The Ultimate QT Infograph";
    this.edition = "ENTERPRISE EDITION";

    this.categoryElementMap = {'Emotional': {Quirks:
      ['Adventurous','Ambitious','Analytical','Artistic','Assertive', 'Athletic', 'Confident', 'Creative',
       'Cutesy', 'Cynical', 'Easy-going', 'Empathetic', 'Energetic', 'Honest', 'Humorous', 'Hygienic',
       'Intelligent', 'Kind', 'Lazy', 'Loud', 'Materialistic', 'Messy', 'Outdoorsy', 'Passionate',
       'Reliable', 'Resourceful', 'Romantic', 'Serious', 'Sexual', 'Social', 'Talkative', 'Wise']
    }};

    this.targets = [];
    var possibleTargets = ["You","Them"]
    for (var i=0;i<possibleTargets.length;i++) {
      this.targets.push(<Target key={possibleTargets[i]} targetName={possibleTargets[i]} categoryElementMap={this.categoryElementMap} />);
    }
  }

  render() {
    return (
      <div className="chart">
        <ReactBootstrap.Grid>
          <ReactBootstrap.Row>
            <ReactBootstrap.Col>
              <div className="chartName">
                <h1 style={{'textAlign': 'center'}}>{this.tagLine}</h1>
                <h4 style={{'textAlign': 'center'}}>{this.edition}</h4>
              </div>
              {this.targets}
            </ReactBootstrap.Col>
          </ReactBootstrap.Row>
        </ReactBootstrap.Grid>
      </div>
    );
  }
}

class Target extends React.Component {
  constructor (props) {
    super(props);

    if (this.props.targetName.toLowerCase()!="you" && this.props.targetName.toLowerCase()!="them") {
      throw "Target must be either \'You\' or \'Them\', received: " + this.props.targetName;
    }

    this.categories = [];

    for (var categoryName in props.categoryElementMap) {
      this.categories.push(<Category categoryName={categoryName} elementMap={props.categoryElementMap[categoryName]} youOrThem={this.props.targetName} />);
    }
  }

  render() {
    return (
      <div className="target">
        <ReactBootstrap.Grid>
          <ReactBootstrap.Row>
            <ReactBootstrap.Col>
              <div className="targetName">
                <h2>{this.props.targetName}</h2>
              </div>
            </ReactBootstrap.Col>
          </ReactBootstrap.Row>
        </ReactBootstrap.Grid>
        {this.categories}
      </div>
    );
  }
}

class Category extends React.Component {
  constructor(props) {
    super(props);

    this.elements = [];

    for (var elementName in this.props.elementMap) {
      this.elements.push(<MulticolorCheckboxSet name={elementName} labels={this.props.elementMap[elementName]} youOrThem={this.props.youOrThem} />); //TODO: change this when MulticolorCheckboxSet becomes an Element subclass
    }
  }

  render() {
    return (
      <div className="category">
        <ReactBootstrap.Grid>
          <ReactBootstrap.Row>
            <ReactBootstrap.Col>
              <div className="categoryName">
                <h3>{this.props.categoryName}</h3>
              </div>
            </ReactBootstrap.Col>
          </ReactBootstrap.Row>
        </ReactBootstrap.Grid>
        {this.elements}
      </div>
    );
  }
}

class MulticolorCheckboxSet extends React.Component {
  constructor(props) {
    super(props);

    this.checkboxes     = this.getCheckboxes();
    this.gridCheckboxes = this.fillGrid(MulticolorCheckboxSet.colsDesktop,this.checkboxes);
  }

  static get colsDesktop()   {return 4;}
  static get numColsMedium() {return 2;}

  getCheckboxes() {
    this.props.labels.sort()

    var checkboxes = [];
    for (var i=0; i<this.props.labels.length; i++) {
      checkboxes.push(<MulticolorCheckbox label={this.props.labels[i]} youOrThem={this.props.youOrThem} pickOneIfYou={false} />);
    }

    return checkboxes;
  }

  fillGrid(numColsDesktop,elements) {
    var rows = [];
    for (var i=0;i<Math.ceil(elements.length/numColsDesktop);i++) {
      rows.push(this.fillRow(numColsDesktop,elements.slice(numColsDesktop*i,numColsDesktop*(i+1)))); //still works when there's only a few elements left for the last row
    }

    return (
      <div className="multicolorCheckboxes">
        <ReactBootstrap.Grid>
          {rows}
        </ReactBootstrap.Grid>
      </div>
    );
  }

  fillRow(numColsDesktop,rowElements) {
    if(rowElements.length>numColsDesktop) {
      throw "Cannot fit more elements into a row than there are columns."
    }

    var cols = [];
    for(var i=0;i<numColsDesktop;i++) {
      if (i<rowElements.length) {
        cols.push(this.fillColumn(numColsDesktop,rowElements[i]));
      }
    }

    return (
      <ReactBootstrap.Row>
        {cols}
      </ReactBootstrap.Row>
    );
  }

  fillColumn(numColsDesktop,element) {
    if (typeof element!==undefined) { //TODO: figure out if this is necessary
      return (
        <ReactBootstrap.Col lg={Math.floor(12/numColsDesktop)} md={Math.floor(12/MulticolorCheckboxSet.numColsMedium)}>
          {element}
        </ReactBootstrap.Col>
      );
    }
  }

  render() { //the grid is wrapped in another div by fillGrid
    return (
      <div className="multicolorCheckboxSet">
        <ReactBootstrap.Grid>
          <ReactBootstrap.Row>
            <ReactBootstrap.Col lg={12}>
              <label class="multicolorCheckboxSetName"><span><h4>{this.props.name}</h4></span></label>
            </ReactBootstrap.Col>
          </ReactBootstrap.Row>
        </ReactBootstrap.Grid>
        {this.gridCheckboxes}
      </div>
    );
  }
}

class MulticolorCheckbox extends React.Component {
  static colorNames(index) { return(['red','orange','yellow','green','blue','pink'][index]); }

  static get youMulticolorLabels()  { return ['Very Poorly', 'Poorly', 'Somewhat Accurately', 'Accurately', 'Very Accurately']; }
  static get themMulticolorLabels() { return ['Awful', 'Bad', 'Acceptable', 'Good', 'Very Good', 'Perfect']; }

  constructor(props) {
    super(props);

    this.makeSelection = this.makeSelection.bind(this); //ensure callbacks have the proper context

    var descriptors = [];
    var footerInitial;
    if ((this.props.youOrThem.toLowerCase()=='you' && !this.props.pickOneIfYou) || this.props.youOrThem.toLowerCase()=='them') {
      if (this.props.youOrThem.toLowerCase()=='you') { //present all colors except pink
        descriptors   = MulticolorCheckbox.youMulticolorLabels;
        footerInitial = 'Describes me'
      } else { //present all colors including pink
        descriptors = MulticolorCheckbox.themMulticolorLabels;
        footerInitial = 'I consider this'
      }
    } else {
      throw "Multicolor checkboxes cannot be \'pick one\'.";
    }

    var footer = 'Select one.';

    var childColors = [];
    for (var i=0; i<descriptors.length; i++) {
      childColors[i] = MulticolorCheckbox.colorNames(i);
    }

    this.state = {
      footerInitial: footerInitial,
      footer: footer,
      descriptors: descriptors,
      childColors: childColors
    };
  }

  makeSelection(index) {
    this.setState( {footer: this.state.footerInitial + ' ' + this.state.descriptors[index].toLowerCase() + '.'} ); //set the footer as appropriate

    var childColorsTmp = []; //reset the other checkbox choices' colors, and change the color of the new selection
    for (var i=0;i<this.state.childColors.length;i++) {
      childColorsTmp[i] = MulticolorCheckbox.colorNames(i);
    }
    childColorsTmp[index] = 'black';
    this.setState( {childColors: childColorsTmp} );
  }

  render() {
    var choices = [];
    var percentWidth = 100 / this.state.descriptors.length;
    for (var i=0; i<this.state.descriptors.length; i++) {
      var side;
      var text;
      if (i==0) {
        side = 'left';
        text = '-';
      } else if (i==this.state.descriptors.length-1) {
        side = 'right';
        text = '+';
      } else {
        side = 'middle';
        text = '';
      }

      console.log(this.state.childColors[i]);
      choices.push(<CheckboxChoice label={this.props.label} side={side} colorName={this.state.childColors[i]} colorScore={i} text={text} onClick={this.makeSelection} percentWidth={percentWidth} textHidden={true} />);
    }

    //TODO: the extra line breaks here are a hideous kludge
    return (
      <div className="multicolorCheckbox">
        <label class="multicolorCheckboxLabel"><span><b>{this.props.label + ': '}</b></span></label>
        <br />
        {choices}
        <br />
        <br />
        <span>{this.state.footer}</span>
      </div>
    );
  }
}

class CheckboxChoice extends React.Component {
  render() {
    return ( //TODO: figure out how to add multiple optional classes
      <label className={'checkboxChoice' + ' ' + this.props.colorName + ' ' + this.props.side} style={{width: this.props.percentWidth + "%"}}><input type="radio" name={this.props.label} value={this.props.colorScore} onClick={() => this.props.onClick(this.props.colorScore)} /><span>{this.props.text}</span></label>
    );
  }
}

ReactDOM.render(
  <Chart />,
  document.getElementById('root')
);

/*
class Category extends React.Component {

}

class SelectOneFuzzyRangeBar extends React.Component {
  render() {
    var cells;
    for (var i=0; i<this.props.numCells; i++) {
      cells.push(<BinaryColorChoice label={this.props.name} score={i} />);
    }

    return (
      <div className="selectOneFuzzyBar">
        <label class="groupLabel"><span>{this.props.name}</span></label>
        <div className="binaryColorChoices">
          {cells}
        </div>
      </div>
    );
  }
}

class SelectAllFuzzyRangeBar extends React.Component {
  render() {
    var choices;

    for (var i=0;i<this.props.numChoices;i++) {
      var extraClasses = [];
      var text = '';
      if (i==0) {
        extraClasses.push('leftmostChoice');
        text = this.props.leftText;
      } else if {
        extraClasses.push('rightmostChoice');
        text = this.props.rightText;
      }

      choices.push(<DropdownColorChoice displayText=text />);
    }

    return (
      <div className="selectAllFuzzyBar">
  			<label class="elementLabel"><span>Extroversion:</span></label>
  			<div class="selectAllFuzzyBarChoices">
          {choices}
        </div>
      </div>
    );
  }
}

class BinaryColorChoice extends React.Component {
  render() {
    return (
      <label class="selectOneCell"><input type="radio" name={this.props.label} value={this.props.score}><span>{this.props.text}</span></label>
    );
  }
}

class DropdownColorChoice extends React.Component {
  var colorNames = ['red',     'orange',  'yellow',  'green',   'blue',    'pink'];
  var colorCodes = ['#ff0000', '#ff7200', '#ffff00', '#00ff00', '#0000ff', '#ff00ff'];

  var textLabels = ['Perfect', 'Very Good', 'Good', 'Acceptable', 'Bad', 'Awful'];

  render() {
    var options;
    for (var i=0; i<colorNames.length; i++) {
      options.push(<option class={colorNames[i]} value={colorCodes[i]}><span>{textlabels[i]}</span></option>);
    }

    return (
      <select>
        {options}
      </select>
    );
  }
}

//gender, body type, race etc.
class SelectOneCheckboxSet extends React.Component {
  var selectedColor   = 'green'
  var unselectedColor = 'red'

  render() {
    var checkboxChoices;

    this.props.labels.sort();
    for (var i=0; i<labels.length; i++) {
      choices.push(<CheckboxChoice label=this.props.name color=unselectedColor colorScore=this.props.labels[i] text=this.props.labels[i] textHidden=false />);
    }

    return (
      <div className="selectOneCheckboxSet">
        <label class="selectOneCheckboxSetName"><span>{this.props.name}</span></label>
        {checkboxChoices}
      </div>
    );
  }
}

*/
