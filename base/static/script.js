import { h, Component, render } from './preact-10.0.0.js';

const PROGRAM_PLAN = {
  'name': 'Basic 3-workout 5x5',
  'workouts': [
    {
      name: 'Workout A',
      exercises: [
        {
          name: 'Low bar squat',
          weight: 225,
          workSets: [5, 5, 5, 5, 5],
        },
        {
          name: 'Bench press',
          weight: 155,
          workSets: [5, 5, 5, 5, 5],
        },
        {
          name: 'Power clean',
          weight: 85,
          workSets: [3, 3, 3, 3, 3],
        },
      ]
    },
    {
      name: 'Workout B',
      exercises: [
        {
          name: 'Front squat',
          weight: 45,
          workSets: [5, 5, 5, 5, 5],
        },
        {
          name: 'Skullcrusher',
          weight: 45,
          workSets: [10, 10, 10],
        },
        {
          name: 'Pendlay row',
          weight: 155,
          workSets: [5, 5, 5, 5, 5],
        },
      ],
    },
    {
      name: 'Workout C',
      exercises: [
        {
          name: 'Deadlift',
          weight: 225,
          workSets: [5],
        },
        {
          name: 'Overhead press',
          weight: 90,
          workSets: [5, 5, 5, 5, 5],
        },
        {
          name: 'Pull up',
          weight: 0,
          workSets: [5, 5, 5, 5, 5],
        }
      ],
    }
  ],
};

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
  render() {
    let workouts = PROGRAM_PLAN.workouts.map(workout => h(
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
  state = {
    workoutPlan: null,
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
