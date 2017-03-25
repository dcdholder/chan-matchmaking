class BooleanBar extends React.Component {
  render() {
    return (

    );
  }
}

class NumericalRangeBar extends React.Component {
  render() {
    return (

    );
  }
}

class FuzzyRangeBar extends React.Component {
  render() {
    return (

    );
  }
}

class DropdownColorChoice extends React.Component {
  render() {
    return (

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
    for (i=0; i<labels.length; i++) {
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

class MulticolorCheckboxSet extends React.Component {
  render() {
    var checkboxes;

    this.props.labels.sort()
    for (i=0; i<labels.length; i++) {
      checkboxes.push(<MulticolorCheckbox label={this.props.labels[i]} youOrThem={this.props.youOrThem} pickOneIfYou={this.props.pickOneIfYou} />);
    }

    return (
      <div className="multicolorCheckboxSet">
        <label class="multicolorCheckboxSetName"><span>{this.props.name}</span></label>
        {checkboxes}
      </div>
    );
  }
}

class MulticolorCheckbox extends React.Component {
  var colorNames = ['red','orange','yellow','green','blue','pink'];

  var youMulticolorLabels  = ['Very Poorly', 'Poorly', 'Somewhat Accurately', 'Accurately', 'Very Accurately'];
  var themMulticolorLabels = ['Perfect', 'Very Good', 'Good', 'Acceptable', 'Bad', 'Awful'];

  render() {
    if ((this.props.youOrThem=='you' && this.props.pickOneIfYou) || this.props.youOrThem=='them') {
      var descriptors;
      if (this.props.youOrThem=='you') { //present all colors except pink
        descriptors = youMulticolorLabels;
      } else { //present all colors including pink
        descriptors = themMulticolorLabels;
      }

      var choices;
      for (i=0; i<descriptors.length; i++) {
        var extraClasses = [colorNames[i]];
        if (i==0) {
          extraClasses.push('leftmostChoice');
        } else if (i==descriptors.length-1) {
          extraClasses.push('rightmostChoice');
        }

        choices.push(<CheckboxChoice label=this.props.label color=colorNames[i] colorScore=i text=descriptors[i] textHidden=true />);
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

class CheckboxChoice extends React.Component {
  render() {
    var classes = ['checkboxChoice', this.props.colorName];

    if (this.props.textHidden) {
      classes.push('textHidden')
    }

    return (
      <label className="{this.classes}"><input type="radio" name="{this.props.label}" value="{this.props.colorScore}"><span>{this.props.text}</span></label>
    );
  }
}
