import { h, Component, render } from './preact-10.0.0.js';


class RepRecorder extends Component {
  state = {
    completed: null
  }

  render() {
    let handleClick = e => {
      if(this.state.completed === null) {
        this.setState({ completed: this.props.planned });
        return;
      }

      if(this.state.completed === 0) {
        this.setState({ completed: null });
        return;
      }

      this.setState({ completed: this.state.completed - 1 });
    };

    let display = this.state.completed === null
      ? this.props.planned
      : this.state.completed;

    let className = 'rep-recorder ';

    if(this.state.completed === null) {
      className += 'planned';
    } else if(this.state.completed === this.props.planned) {
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
      { planned: set },
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

class WorkoutPlan extends Component {
  render() {
    let exercises = this.props.workoutPlan.exercises.map(exercise => {
      return h(ExercisePlan, { exercise: exercise });
    });
    return h(
      'div',
      {},
      h('h1', {}, this.props.workoutPlan.name),
      exercises,
      h(
        Button,
        {
          onClick: this.props.onFinished,
          text: 'Finish',
        },
      ),
    );
  }
}

class WorkoutPlanPickerButton extends Component {
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

    return h(
      'div',
      {
        className: 'button workout-plan-picker-button',
        onClick: handleClick,
      },
      h(
        'div',
        { className: 'workout-plan-name' },
        this.props.workout.name,
      ),
      exercises,
    );
  }
}

class WorkoutPlanPicker extends Component {
  constructor(props) {
    super(props);

    this.state = {
      programWorkouts: null
    };

    fetch('/api/program/workout/').then(response => {
      if(!response.ok) {
        throw Error(response.statusText);
      }

      return response.json();
    }).then(responseJson => {
      this.setState({ programWorkouts: responseJson.workouts });
    });
  }

  render() {
    if(this.state.programWorkouts === null) return '';

    let workouts = this.state.programWorkouts.map(workout => h(
      WorkoutPlanPickerButton,
      {
        onClick: this.props.onWorkoutPlanPicked,
        workout: workout,
      },
    ));
    return h(
      'div',
      {},
      h(
        'p',
        {},
        'Which workout would you like to do today?',
        workouts,
      ),
    );
  }
}

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      workoutPlan: null,
    };

  }

  render() {
    if(this.state.workoutPlan === null) {
      let handleWorkoutPlanPicked = workoutPlan => this.setState({
        workoutPlan: workoutPlan,
      });

      return h(
        WorkoutPlanPicker,
        {
          onWorkoutPlanPicked: handleWorkoutPlanPicked,
          program: this.state.program,
        },
      );
    }

    return h(
      WorkoutPlan,
      {
        onFinished: e => this.setState({ workoutPlan: null }),
        workoutPlan: this.state.workoutPlan,
      },
    );
  }
}

render(h(App), document.getElementById('app'));
