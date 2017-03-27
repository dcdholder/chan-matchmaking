//import React, { Component } from 'react';

class Chart extends React.Component {
  constructor (props) { //TODO: change this to a yaml parser when you're done testing out the basic UI
    super(props);

    this.tagLine = "The Ultimate QT Infograph";
    this.edition = "Enterprise Edition";

    this.categoryElementMap = {'Emotional': {Quirks: ['Adventurous','Ambitious','Analytical','Artistic','Assertive', 'Athletic', 'Confident', 'Creative', 'Cutesy']}};

    this.targets = [];
    var possibleTargets = ["You","Them"]
    for (var i=0;i<possibleTargets.length;i++) {
      this.targets.push(<Target key={possibleTargets[i]} targetName={possibleTargets[i]} categoryElementMap={this.categoryElementMap} />);
    }
  }

  render() {
    return (
      <div className="chart">
        <div class="row">
          <div class="col-lg-12">
            <h1>{this.tagLine}</h1>
            <h4>{this.edition}</h4>
          </div>
        </div>
        {this.targets}
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
        <div class="row">
          <div class="col-lg-12">
            <h2>{this.props.targetName}</h2>
          </div>
        </div>
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
        <div class="row">
          <div class="col-lg-12">
            <h3>{this.props.categoryName}</h3>
          </div>
        </div>
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

  static get colsDesktop() {return 4;}

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
        {rows}
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
      <div class="row">
        {cols}
      </div>
    );
  }

  fillColumn(numColsDesktop,element) {
    if (typeof element===undefined) { //TODO: figure out if this is necessary
      return (
        <div class="col-lg-{numColsDesktop}">
        </div>
      );
    } else {
      return (
        <div class="col-lg-{numColsDesktop}">
          {element}
        </div>
      );
    }
  }

  render() { //the grid is wrapped in another div by fillGrid
    return (
      <div className="multicolorCheckboxSet">
        <label class="multicolorCheckboxSetName"><span>{this.props.name}</span></label>
        {this.gridCheckboxes}
      </div>
    );
  }
}

class MulticolorCheckbox extends React.Component {
  static colorNames(index) { return(['red','orange','yellow','green','blue','pink'][index]); }

  static get youMulticolorLabels()  { return ['Very Poorly', 'Poorly', 'Somewhat Accurately', 'Accurately', 'Very Accurately']; }
  static get themMulticolorLabels() { return ['Awful', 'Bad', 'Acceptable', 'Good', 'Very Good', 'Perfect']; }

  render() {
    if ((this.props.youOrThem.toLowerCase()=='you' && !this.props.pickOneIfYou) || this.props.youOrThem.toLowerCase()=='them') {
      var descriptors;
      if (this.props.youOrThem.toLowerCase()=='you') { //present all colors except pink
        descriptors = MulticolorCheckbox.youMulticolorLabels;
      } else { //present all colors including pink
        descriptors = MulticolorCheckbox.themMulticolorLabels;
      }

      var choices = [];
      for (var i=0; i<descriptors.length; i++) {
        var extraClasses = [];
        if (i==0) {
          extraClasses.push('leftmostChoice');
        } else if (i==descriptors.length-1) {
          extraClasses.push('rightmostChoice');
        }

        choices.push(<CheckboxChoice label={this.props.label} colorName={MulticolorCheckbox.colorNames(i)} colorScore={i} text={descriptors[i]} textHidden={true} />);
      }

      return (
        <div className="multicolorCheckbox">
          <label class="multicolorCheckboxLabel"><span>{this.props.label + ': '}</span></label>
          {choices}
        </div>
      );
    } else {
      throw "Multicolor checkboxes cannot be \'pick one\'.";
    }
  }
}

class CheckboxChoice extends React.Component {
  render() {
    var classes = ['checkboxChoice', this.props.colorName];

    if (this.props.textHidden) {
      classes.push('textHidden');
    }

    return ( //TODO: figure out how to add multiple optional classes
      <label className="checkboxChoice"><input type="radio" name={this.props.label} value={this.props.colorScore} /><span>{this.props.text}</span></label>
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
