from httpie.output.ui.man_pages import is_available


def test_is_available_returns_false_on_windows(monkeypatch):
    monkeypatch.setattr("httpie.output.ui.man_pages.sys.platform", "win32")
    assert is_available("http") is False


def test_is_available_honors_no_man_pages_env(monkeypatch):
    monkeypatch.setattr("httpie.output.ui.man_pages.NO_MAN_PAGES", True)
    monkeypatch.setattr("httpie.output.ui.man_pages.sys.platform", "linux")
    assert is_available("http") is False


def test_is_available_returns_true_when_man_succeeds(monkeypatch):
    monkeypatch.setattr("httpie.output.ui.man_pages.sys.platform", "linux")

    class CompletedProcess:
        returncode = 0

    monkeypatch.setattr(
        "httpie.output.ui.man_pages.subprocess.run",
        lambda *args, **kwargs: CompletedProcess(),
    )
    assert is_available("http") is True


def test_is_available_returns_false_when_man_fails(monkeypatch):
    monkeypatch.setattr("httpie.output.ui.man_pages.sys.platform", "linux")

    class CompletedProcess:
        returncode = 1

    monkeypatch.setattr(
        "httpie.output.ui.man_pages.subprocess.run",
        lambda *args, **kwargs: CompletedProcess(),
    )
    assert is_available("http") is False


def test_is_available_returns_false_when_man_raises(monkeypatch):
    monkeypatch.setattr("httpie.output.ui.man_pages.sys.platform", "linux")

    def raise_error(*args, **kwargs):
        raise OSError("no man")

    monkeypatch.setattr("httpie.output.ui.man_pages.subprocess.run", raise_error)
    assert is_available("http") is False
