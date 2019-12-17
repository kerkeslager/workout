import { h, Component, render } from './preact-10.0.0.js';

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

class RepRecorder extends Component {
  constructor(props) {
    super(props);
    this.state = props.setRecord;
  }

  render() {
    let handleClick = e => {
      let completedReps = undefined;

      if(this.state.completedReps === null) {
        completedReps = this.state.plannedReps;
      } else if(this.state.completedReps === 0) {
        completedReps = null;
      } else {
        completedReps = this.state.completedReps - 1;
      }

      fetch(
        '/api/user/set-record/update/',
        {
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
          },
          method: 'POST',
          body: JSON.stringify({
            setRecord: this.state.id,
            completedReps: completedReps,
          }),
        },
      ).then(response => {
        if(!response.ok) throw Error(response.statusText);
        return response.json();
      }).then(responseJson => {
        this.setState({ completedReps: completedReps });
      });
    };

    let display = this.state.completedReps === null
      ? this.state.plannedReps
      : this.state.completedReps;

    let className = 'rep-recorder ';

    if(this.state.completedReps === null) {
      className += 'planned';
    } else if(this.state.completedReps === this.state.plannedReps) {
      className += 'complete';
    } else {
      className += 'incomplete';
    }

    return h(
      'div',
      {
        className: className,
        onClick: handleClick,
      },
      display,
    );
  }
}

class ExercisePlan extends Component {
  render() {
    let repRecorders = this.props.exercise.workSets.map(set => h(
      RepRecorder,
      { setRecord: set },
    ));

    return h(
      'div',
      { className: 'exercise' },
      h(
        'div',
        {className: 'exercise-name'},
        this.props.exercise.name,
      ),
      h(
        'div',
        {className: 'weight'},
        this.props.exercise.weight,
        'lbs',
      ),
      h(
        'div',
        { className: 'rep-recorder-list' },
        repRecorders,
      ),
    );
  }
}

class Button extends Component {
  render() {
    return h(
      'div',
      {
        className: 'button',
        onClick: this.props.onClick,
      },
      this.props.text,
    );
  }
}
Button.defaultProps = {
  onClick: e => null,
};

class WorkoutRecord extends Component {
  constructor(props) {
    super(props);

    this.state = {
      workoutRecord: null
    };

    this.loadWorkoutRecord();
  }

  loadWorkoutRecord() {
    fetch(
      '/api/user/workout-record/start/',
      {
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),
        },
        method: 'POST',
        body: JSON.stringify({ programWorkout: this.props.programWorkoutId }),
      },
    ).then(response => {
      if(!response.ok) throw Error(response.statusText);
      return response.json();
    }).then(responseJson => {
      this.setState({ workoutRecord: responseJson });
    });
  }

  render() {
    if(this.state.workoutRecord === null) return '';

    let exercises = this.state.workoutRecord.exercises.map(exercise => {
      return h(ExercisePlan, { exercise: exercise });
    });

    let handleClick = e => {
      fetch(
        '/api/user/workout-record/finish/',
        {
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
          },
          method: 'POST',
          body: JSON.stringify({
            workoutRecord: this.state.workoutRecord.id,
          }),
        },
      ).then(response => {
        if(!response.ok) throw Error(response.statusText);
        return response.json();
      }).then(responseJson => {
        this.props.onFinished();
      });
    };

    return h(
      'div',
      {},
      h(
        'h1',
        {},
        this.state.workoutRecord.name
      ),
      exercises,
      h(
        Button,
        {
          onClick: handleClick,
          text: 'Finish',
        },
      ),
    );
  }
}

class ProgramWorkoutPickerButton extends Component {
  render() {
    let exercises = this.props.workout.exercises.map(exercise => {
      // If all workSets are equal, show in sets x reps form.
      let displaySets = exercise.workSets.every(set => set === exercise.workSets[0])
        ? exercise.workSets.length + ' x ' + exercise.workSets[0]
        : exercise.workSets.join(', ');

      return h(
        'div',
        {},
        displaySets,
        ' ',
        exercise.name,
      );
    });

    let handleClick = e => this.props.onClick(this.props.workout);

    let ongoingDisplay = this.props.workout.ongoing
      ? ' (Ongoing)'
      : '';

    return h(
      'div',
      {
        className: 'button workout-plan-picker-button',
        onClick: handleClick,
      },
      h(
        'div',
        { className: 'workout-plan-name' },
        this.props.workout.name + ongoingDisplay,
      ),
      exercises,
    );
  }
}

class ProgramWorkoutPicker extends Component {
  constructor(props) {
    super(props);

    this.state = {
      recommendedProgramWorkouts: null,
      otherProgramWorkouts: null
    };

    this.loadProgramWorkouts();
  }

  loadProgramWorkouts() {
    fetch('/api/program/workout/recommend/').then(response => {
      if(!response.ok) {
        throw Error(response.statusText);
      }

      return response.json();
    }).then(responseJson => {
      this.setState({
        recommendedProgramWorkouts: responseJson.recommended,
        otherProgramWorkouts: responseJson.other,
      });
    });
  }

  render() {
    if(this.state.recommendedProgramWorkouts === null || this.state.otherProgramWorkouts === null)
      return '';

    let renderProgramWorkout = workout => h(
      ProgramWorkoutPickerButton,
      {
        onClick: this.props.onProgramWorkoutPicked,
        workout: workout,
      },
    );

    let recommendedProgramWorkouts = this.state.recommendedProgramWorkouts.map(renderProgramWorkout);
    let otherProgramWorkouts = this.state.otherProgramWorkouts.map(renderProgramWorkout);

    let recommendedDisplay = recommendedProgramWorkouts.length > 0
      ? [
        h('p', {}, h('strong', {}, 'Recommended')),
        recommendedProgramWorkouts,
      ]
      : h('i', {}, "Please choose a program to get workout recommendations");

    let otherDisplay = otherProgramWorkouts.length > 0
      ? [
        h('p', {}, h('strong', {}, 'Other')),
        otherProgramWorkouts,
      ]
      : '';

    return h(
      'div',
      {},
      h('p', {}, 'Which workout would you like to do today?'),
      recommendedDisplay,
      otherDisplay,
    );
  }
}

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      programWorkoutId: null,
    };

  }

  render() {
    if(this.state.programWorkoutId === null) {
      let handleProgramWorkoutPicked = programWorkout => this.setState({
        programWorkoutId: programWorkout.id,
      });

      return h(
        ProgramWorkoutPicker,
        {
          onProgramWorkoutPicked: handleProgramWorkoutPicked,
          program: this.state.program,
        },
      );
    }

    return h(
      WorkoutRecord,
      {
        onFinished: e => this.setState({ programWorkoutId: null }),
        programWorkoutId: this.state.programWorkoutId,
      },
    );
  }
}

render(h(App), document.getElementById('app'));
