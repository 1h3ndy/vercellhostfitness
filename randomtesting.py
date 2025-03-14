from flask import Flask, render_template, session, redirect, url_for, request, flash, jsonify
import sqlite3
from markupsafe import escape

from datetime import datetime, timedelta


@app.route('/weight-log')
def weight_log():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('weight_log.html')
