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

class SetRecord extends Component {
  render() {
    let className = 'button set-record ';

    if(this.props.setRecord.completedReps === null) {
      className += 'planned';
    } else if(this.props.setRecord.completedReps === this.props.setRecord.plannedReps) {
      className += 'complete';
    } else {
      className += 'incomplete';
    }

    let onClick = e => {
      let completedReps = undefined;

      if(this.props.setRecord.completedReps === null) {
        completedReps = this.props.setRecord.plannedReps;
      } else if(this.props.setRecord.completedReps === 0) {
        completedReps = null;
      } else {
        completedReps = this.props.setRecord.completedReps - 1;
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
            setRecord: this.props.setRecord.id,
            completedReps: completedReps,
          }),
        },
      ).then(response => {
        if(!response.ok) throw Error(response.statusText);
        return response.json();
      }).then(responseJson => {
        let setRecord = immer.produce(
          this.props.setRecord,
          setRecord => {
            setRecord.completedReps = completedReps;
          },
        );
        this.props.onChanged(setRecord);
      });
    };

    let display = this.props.setRecord.completedReps === null
      ? this.props.setRecord.plannedReps
      : this.props.setRecord.completedReps;

    return h(
      'div',
      {
        className: className,
        onClick: onClick,
      },
      display,
    );
  }
}

class SetRecordList extends Component {
  render() {
    let setRecords = this.props.setRecords.map(setRecord => h(
      SetRecord,
      {
        onChanged: this.props.onSetRecordChanged,
        setRecord: setRecord,
      },
    ));

    return h(
      'div',
      { className: 'set-record-list-at-weight' },
      h(
        'div',
        {className: 'weight'},
        this.props.weight,
        'lbs',
      ),
      h(
        'div',
        { className: 'set-record-list' },
        setRecords,
      ),
    );
  }
}

class ExerciseRecord extends Component {
  constructor(props) {
    super(props);

    this.state = {
      isChangeWeightModalVisible: false,
    };
  }

  render() {
    let onSetRecordChanged = setRecord => {
      let exerciseRecord = immer.produce(
        this.props.exercise,
        exerciseRecord => {
          let index = this.props.exercise.workSets.findIndex(
            sr => sr.id === setRecord.id,
          );

          if(index != -1) exerciseRecord.workSets[index] = setRecord;

          index = this.props.exercise.warmupSets.findIndex(
            sr => sr.id === setRecord.id,
          );

          if(index != -1) exerciseRecord.warmupSets[index] = setRecord;
        },
      );
      this.props.onChanged(exerciseRecord);
    };

    let showChangeWeightModal = e => {
      e.preventDefault();

      this.setState({ isChangeWeightModalVisible: true });
    };

    let changeWeightModal = null;

    if(this.state.isChangeWeightModalVisible) {
      let handleWeightChanged = () => {
        let weight = document.getElementById('weight-change-input').valueAsNumber;

        if(weight != this.props.exercise.weight) {
          fetch(
            '/api/user/exercise-record/update/',
            {
              headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
              },
              method: 'POST',
              body: JSON.stringify({
                exerciseRecord: this.props.exercise.id,
                weight: weight,
              }),
            },
          ).then(response => {
            if(!response.ok) {
              throw Error(response.statusText);
            }
            return response.json();
          }).then(responseJson => {
            this.props.onChanged(responseJson.exerciseRecord);
          });
        }

        this.setState({ isChangeWeightModalVisible: false });
      };
      changeWeightModal = h(
        Modal,
        {},
        h(
          'div',
          { className: 'warning' },
          'WARNING: Changing your work weight will generate a new warmup and delete any warmup or work sets that you have already completed.',
        ),
        h(
          'input',
          {
            id: 'weight-change-input',
            step: 5,
            type: 'number',
            value: this.props.exercise.weight,
          },
        ),
        ' lbs',
        h(
          'div',
          { className: 'button-panel' },
          h(
            Button,
            {
              onClick: handleWeightChanged,
              text: 'Change',
            },
          ),
          h(
            Button,
            {
              onClick: e => this.setState({ isChangeWeightModalVisible: false }),
              text: 'Cancel',
            },
          ),
        ),
      );
    }

    let isWarmedUp = this.props.exercise.warmupSets.every(
      setRecord => setRecord.completedReps === setRecord.plannedReps
    );

    if(!isWarmedUp && !(this.props.exercise.skipWarmup)) {
      let skipWarmup = e => {
        e.preventDefault();
        let exerciseRecord = immer.produce(
          this.props.exercise,
          exerciseRecord => { exerciseRecord.skipWarmup = true; }
        );
        this.props.onChanged(exerciseRecord);
      };

      let warmupSetRecordGroups = this.props.exercise.warmupSets.map(setRecord => h(
        SetRecordList,
        {
          onSetRecordChanged: onSetRecordChanged,
          setRecords: [setRecord],
          weight: setRecord.weight,
        }
      ));

      return h(
        'div',
        { className: 'exercise' },
        h(
          'div',
          {className: 'name'},
          this.props.exercise.name,
          ' ',
          h(
            'a',
            {
              href: '',
              onClick: showChangeWeightModal,
            },
            '(' + this.props.exercise.weight + 'lbs)',
          ),
        ),
        h(
          'div',
          { className: 'warmup' },
          h(
            'div',
            {
              className: 'info',
            },
            'Warmup',
            h(
              'a',
              {
                href: '',
                onClick: skipWarmup,
              },
              '(Skip)',
            ),
          ),
          h(
            'div',
            { className: 'sets' },
            warmupSetRecordGroups,
          ),
        ),
        changeWeightModal,
      );
    }

    return h(
      'div',
      { className: 'exercise' },
      h(
        'div',
        {className: 'name'},
        this.props.exercise.name,
        ' ',
        h(
          'a',
          {
            href: '',
            onClick: showChangeWeightModal,
          },
          '(' + this.props.exercise.weight + 'lbs)',
        ),
      ),
      h(
        SetRecordList,
        {
          onSetRecordChanged: onSetRecordChanged,
          setRecords: this.props.exercise.workSets,
          weight: this.props.exercise.weight,
        },
      ),
      changeWeightModal,
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

class Modal extends Component {
  render() {
    return h(
      'div',
      {
        className: 'modal',
      },
      this.props.children,
    );
  }
}

class WorkoutRecord extends Component {
  constructor(props) {
    super(props);

    this.state = {
      showConfirmFinishIncompleteWorkout: false,
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

  finishWorkout() {
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
  }

  render() {
    if(this.state.workoutRecord === null) return '';

    let onExerciseChanged = exerciseRecord => {
      let workoutRecord = immer.produce(
        this.state.workoutRecord,
        workoutRecord => {
          let index = this.state.workoutRecord.exercises.findIndex(
            ex => ex.id === exerciseRecord.id
          );

          workoutRecord.exercises[index] = exerciseRecord;
        },
      );
      this.setState({ workoutRecord: workoutRecord });
    };

    let exercises = this.state.workoutRecord.exercises.map(exercise => {
      return h(
        ExerciseRecord,
        {
          exercise: exercise,
          onChanged: onExerciseChanged,
        },
      );
    });

    let handleClick = e => {
      let isWorkoutComplete = this.state.workoutRecord.exercises.every(
        exerciseRecord => exerciseRecord.workSets.every(
          setRecord => setRecord.completedReps !== null
        )
      );

      if(isWorkoutComplete) this.finishWorkout();
      else this.setState({ showConfirmFinishIncompleteWorkout: true });
    };

    let modal = null;

    if(this.state.showConfirmFinishIncompleteWorkout) {
      modal = h(
        'div',
        { className: 'modal' },
        'You have not completed this workout. Are you sure you want to finish it?',
        h(
          'div',
          { className: 'button-panel' },
          h(
            'div',
            {
              className: 'button',
              onClick: e => this.finishWorkout()
            },
            'Finish',
          ),
          h(
            'div',
            {
              className: 'button',
              onClick: e => this.setState({ showConfirmFinishIncompleteWorkout: false })
            },
            'Cancel',
          ),
        ),
      );
    }

    return h(
      'div',
      {},
      h(
        'h1',
        {},
        this.state.workoutRecord.name
      ),
      exercises,
      modal,
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
