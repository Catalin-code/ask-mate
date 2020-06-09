from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from data_manager import Data
# from datetime import datetime
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './images'


@app.route("/add-question", methods=['GET', 'POST'])
def route_ask():
    if request.method == 'POST':
        image = request.files.get('image', None)
        img_type = None
        if image:
            img_type = image.filename.rsplit('.', 1)[1]
        id = Data.Question.add(
            request.form.get('title'),
            request.form.get('message'),
            img_type
        )
        if image:
            image.filename = f"question_{id}.{img_type}"
            secureName = secure_filename(image.filename)
            image.save(f"{app.config['UPLOAD_FOLDER']}/{secureName}")
        return redirect(url_for('route_question', id=id))
    return render_template('add-question.html')


@app.route("/question/<int:id>/delete")
def route_question_delete(id):
    question = Data.Question.get(key='id', value=id)
    if question['image']:
        try:
            os.remove(f"{app.config['UPLOAD_FOLDER']}/{question['image']}")
        except OSError as exception:
            print(exception)
    Data.Question.delete(id)
    return redirect(url_for('route_list'))


@app.route("/question/<int:id>/edit", methods=['GET', 'POST'])
def route_question_edit(id):
    question = Data.Question.get(key='id', value=id)
    if request.method == 'POST':
        question = Data.Question.get(key='id', value=id)
        title = request.form.get('title')
        message = request.form.get('message')
        image = request.files.get('image', None)
        if image:
            image.filename = f"question_{id}.{image.filename.rsplit('.', 1)[1]}"
            secureName = secure_filename(image.filename)
            image.save(f"{app.config['UPLOAD_FOLDER']}/{secureName}")
            image = secureName
        else:
            image = None
        Data.Question.update(id, title=title, message=message, image=image)
        return redirect(url_for('route_question', id=id))

    return render_template('add-question.html', question=question)


@app.route("/question/<int:id>")
def route_question(id):
    question = Data.Question.get(key='id', value=id)
    answers = Data.Answer.get(key='question_id', value=id)
    comment = Data.Comment.get(key='question_id', value=id)
    tags = Data.Tag.get()
    question_tags = Data.Tag.get(id)
    answer_comments = {}
    for answer in answers:
        answer_comments[answer['id']] = Data.Comment.get(
            key='answer_id', value=answer['id'])
    return render_template('question.html', id=id, question=question, answers=answers, tags=tags, question_tags=question_tags, comments=comment, answer_comments=answer_comments)


@app.route('/question/<int:question_id>/new-answer', methods=['GET', 'POST'])
def route_post_answer(question_id):
    question = Data.Question.get(key='id', value=question_id)
    if request.method == 'POST':
        image = request.files.get('image', None)
        img_type = None
        if image:
            img_type = image.filename.rsplit('.', 1)[1]
        id = Data.Answer.add(
            question_id,
            request.form.get('answer'),
            img_type
        )
        if image:
            image.filename = f"answer_{id}.{img_type}"
            secureName = secure_filename(image.filename)
            image.save(f"{app.config['UPLOAD_FOLDER']}/{secureName}")
        return redirect(url_for('route_question', id=question_id))
    return render_template('answer.html', question=question)


@app.route('/search')
def route_search():
    phrase = request.args.get('q', '')
    questions = Data.Question.get(key='title', value=phrase)
    _questions = Data.Question.get(key='message', value=phrase)
    for q in _questions:
        if q not in questions:
            questions.append(q)
    answers = Data.Answer.get(key='message', value=phrase)
    return render_template('search.html', questions=questions, answers=answers)


@app.route("/image/<name>")
def route_image(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)


@app.route("/", methods=['GET', 'POST'])
def route_index():
    questions = Data.Question.get()
    questions = sorted(questions, key=lambda question: question['submission_time'], reverse=True)[:5]

    questions = sorted(
        questions,
        key=lambda question: question[request.args.get('order_by', 'submission_time')],
        reverse=(request.args.get('order_direction', 'desc') == 'desc')
    )

    if request.method == 'POST':
        pass

    return render_template('index.html', questions=questions, sort_key=request.args.get('order_by'), sort_order=request.args.get('order_direction'))


@app.route("/list")
def route_list():
    questions = Data.Question.get()
    questions = sorted(
        questions,
        key=lambda question: question[request.args.get('order_by', 'submission_time')],
        reverse=(request.args.get('order_direction', 'desc') == 'desc')
    )
    return render_template('list.html', questions=questions, sort_key=request.args.get('order_by'), sort_order=request.args.get('order_direction'))


@app.route('/question/<int:id>/vote_up')
def route_question_vote_up(id):
    Data.Question.update(id, vote='vote_number + 1')
    return redirect(url_for('route_list'))


@app.route('/question/<int:id>/vote_down')
def route_question_vote_down(id):
    Data.Question.update(id, vote='vote_number - 1')
    return redirect(url_for('route_list'))


@app.route('/answer/<int:id>/vote_up')
def route_answer_vote_up(id):
    Data.Answer.update(id, vote='vote_number + 1')
    question_id = Data.Answer.get(key='id', value=id)['question_id']
    return redirect(url_for('route_question', id=question_id))


@app.route('/answer/<int:id>/vote_down')
def route_answer_vote_down(id):
    Data.Answer.update(id, vote='vote_number - 1')
    question_id = Data.Answer.get(key='id', value=id)['question_id']
    return redirect(url_for('route_question', id=question_id))


@app.route('/answer/<int:id>/delete')
def route_delete_answer(id):
    answer = Data.Answer.get(key='id', value=id)
    if answer['image']:
        try:
            os.remove(f"{app.config['UPLOAD_FOLDER']}/{answer['image']}")
        except OSError as exception:
            print(exception)
    Data.Answer.delete(id)
    return redirect(url_for('route_question', id=id))


@app.route('/question/<int:id>/new-comment', methods=['GET', 'POST'])
def route_question_comment(id):
    question = Data.Question.get(key='id', value=id)
    if request.method == 'POST':
        comment = request.form.get('comment')
        Data.Comment.add(comment, question_id=id)
        return redirect(url_for('route_question', id=id))
    return render_template('comment-question.html', question=question)


@app.route('/answer/<int:id>/new-comment', methods=['GET', 'POST'])
def route_answer_comment(id):
    answer = Data.Answer.get(key='id', value=id)
    if request.method == 'POST':
        comment = request.form.get('comment')
        Data.Comment.add(comment, answer_id=id)
        return redirect(url_for('route_question', id=answer['question_id']))
    return render_template('comment-answer.html', answer=answer)


@app.route('/answer/<int:answer_id>/edit', methods=['GET', 'POST'])
def route_edit_answer(answer_id):
    answer = Data.Answer.get(key='id', value=answer_id)[0]
    if request.method == 'POST':
        message = request.form.get('message')
        Data.Answer.update(answer_id, message=message)
        return redirect(url_for('route_question', id=answer['question_id']))
    return render_template('edit_answer.html', answer=answer)


@app.route('/question/<int:id>/new-tag', methods=['POST'])
def route_new_tag(id):
    if request.form.get('type') == 'new':
        tag = request.form.get('new_tag')
        Data.Tag.new(tag)
    elif request.form.get('type') == 'add':
        tag_id = request.form.get('tag')
        Data.Tag.add(id, tag_id)
    return redirect(url_for('route_question', id=id))


@app.route('/question/<int:id>/tag/<int:tag_id>/delete', methods=['GET', 'POST'])
def route_delete_tag(id, tag_id):
    Data.Tag.remove(id, tag_id)
    return redirect(url_for('route_question', id=id))


@app.route('/comment/<int:id>/edit', methods=['GET', 'POST'])
def route_edit_comment(id):
    comment = Data.Comment.get(key='id', value=id)
    if comment['question_id'] is not None:
        question_id = comment['question_id']
    else:
        answer = Data.Answer.get(key='id', value=comment['answer_id'])
        question_id = answer['question_id']
    if request.method == 'POST':
        Data.Comment.update(id, message=request.form.get('comment'), edited_count='edited_count + 1')
        return redirect(url_for('route_question', id=question_id))
    return render_template('comment-edit.html', comment=comment, question_id=question_id)


@app.route('/comments/<int:id>/delete')
def route_delete_comment(id):
    comment = Data.Comment.get(key='id', value=id)
    if comment['question_id'] is not None:
        question_id = comment['question_id']
    else:
        answer = Data.Answer.get(key='id', value=comment['answer_id'])
        question_id = answer['question_id']
    Data.Comment.delete(id)
    return redirect(url_for('route_question', id=question_id))


if __name__ == "__main__":
    app.run(debug=True)
