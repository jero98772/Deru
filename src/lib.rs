use pyo3::prelude::*;
use pyo3::exceptions::PySyntaxError;

/// Formats the sum of two numbers as string.


type Symbol = String;
type List = Vec<PyObject>;
type Number = PyObject;


#[pyfunction]
fn atom(_py: Python, token: &str) -> PyResult<PyObject> {
    if let Ok(num) = token.parse::<i64>() {
        Ok(num.to_object(_py))
    } else if let Ok(num) = token.parse::<f64>() {
        Ok(num.to_object(_py))
    } else {
        Ok(token.to_object(_py))
    }
}

#[pyfunction]
fn read_from_tokens(_py: Python, tokens: Vec<String>) -> PyResult<PyObject> {
    if tokens.is_empty() {
        return Err(PyErr::new::<PySyntaxError, _>("unexpected EOF while reading"));
    }
    let token = &tokens[0];
    if "(" == token {
        let mut l = Vec::new();
        let mut tokens = tokens;
        tokens.remove(0); // remove '('
        while tokens[0] != ")" {
            print!("while");
            l.push(read_from_tokens(_py, tokens.clone())?);
            tokens.remove(0); // remove ')'
        }
        return Ok(l.to_object(_py))
    } else if ")" == token {
        Err(PyErr::new::<PySyntaxError, _>("unexpected )"))
    } else {
        return Ok(atom(_py, token)?)
    }
}

#[pyfunction]
fn tokenize(s: &str) -> Vec<String> {
    s.replace('(', " ( ")
        .replace(')', " ) ")
        .split_whitespace()
        .map(|token| token.to_string())
        .collect()
}

/// A Python module implemented in Rust.
#[pymodule]
fn deruuk(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(tokenize, m)?)?;
    m.add_function(wrap_pyfunction!(read_from_tokens, m)?)?;
    m.add_function(wrap_pyfunction!(atom, m)?)?;

    Ok(())
}
